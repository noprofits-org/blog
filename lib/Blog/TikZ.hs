{-# LANGUAGE OverloadedStrings #-}

-- | Render fenced @tikzpicture@ code blocks to inline SVG at build time.
--
-- A Markdown code block tagged @.tikzpicture@ is compiled with @lualatex@
-- (dynamic memory, handles data-heavy diagrams) and converted to SVG with
-- @dvisvgm@ (which preserves transparency, gradients, and PostScript specials
-- that the old @pdf2svg@ path dropped). The SVG is embedded inline so it scales
-- responsively and stays crisp.
--
-- Failure is graceful: a diagram that won't compile is logged to the build and
-- replaced with a visible error box, instead of aborting the whole site build.
-- Posts without any @tikzpicture@ blocks never shell out, so the site builds
-- fine on a machine with no TeX toolchain installed.
module Blog.TikZ
  ( tikzFilter
  , renderTikz
  , inlineSvg
  ) where

import Data.List (isInfixOf)
import qualified Data.Text as T
import qualified Data.Text.IO as TIO
import Hakyll (Compiler, unsafeCompiler)
import Text.Pandoc.Definition (Block (..), Format (..))
import System.Exit (ExitCode (..))
import System.IO (hPutStrLn, stderr)
import System.IO.Temp (withSystemTempDirectory)
import System.Process (readProcessWithExitCode)

-- | Pandoc filter: replace @.tikzpicture@ code blocks with rendered inline SVG,
-- leaving every other block untouched.
tikzFilter :: Block -> Compiler Block
tikzFilter (CodeBlock (_, classes, _) contents)
  | "tikzpicture" `elem` classes = do
      result <- unsafeCompiler $ renderTikz (T.unpack contents)
      let html = case result of
            Right svg -> "<div class=\"tikz-figure\">" ++ inlineSvg svg ++ "</div>"
            Left err  -> "<div class=\"tikz-error\"><strong>Diagram failed to render.</strong>"
                          ++ "<pre>" ++ escapeHtml err ++ "</pre></div>"
      return $ RawBlock (Format "html") (T.pack html)
tikzFilter block = return block

-- | Drop the XML prolog / DOCTYPE that @dvisvgm@ emits, returning the markup
-- from the opening @\<svg@ tag onward so it is safe to inline in HTML. Pure,
-- so it is unit-testable.
inlineSvg :: String -> String
inlineSvg svg =
  let (_, rest) = T.breakOn "<svg" (T.pack svg)
  in if T.null rest then svg else T.unpack rest

-- | Minimal HTML escaping for the error box.
escapeHtml :: String -> String
escapeHtml = concatMap esc
  where
    esc '&' = "&amp;"
    esc '<' = "&lt;"
    esc '>' = "&gt;"
    esc c   = [c]

-- | LaTeX preamble wrapped around each @tikzpicture@ snippet.
tikzPreamble :: String
tikzPreamble = unlines
  [ "\\documentclass[crop,tikz,border=4pt]{standalone}"
  , "\\usepackage{tikz}"
  , "\\usepackage{pgfplots}"
  , "\\usepackage{amsmath}"
  , "\\usepackage[version=4]{mhchem}"
  , "\\pgfplotsset{compat=1.18}"
  , "\\usepgfplotslibrary{units}"
  , "\\usetikzlibrary{arrows.meta}"
  , "\\usetikzlibrary{patterns,patterns.meta}"
  , "\\usetikzlibrary{backgrounds}"
  , "\\usetikzlibrary{calc}"
  , "\\usetikzlibrary{decorations.pathmorphing}"
  , "\\usetikzlibrary{decorations.markings}"
  , "\\usetikzlibrary{matrix,arrows}"
  , "\\begin{document}"
  ]

-- | Compile a @tikzpicture@ body to SVG via @lualatex@ + @dvisvgm@ in a temp
-- dir. Returns @Left@ with a diagnostic on failure (build continues).
renderTikz :: String -> IO (Either String String)
renderTikz tikzCode = withSystemTempDirectory "blog-tikz" $ \dir -> do
  let texFile = dir ++ "/tikz.tex"
      pdfFile = dir ++ "/tikz.pdf"
      svgFile = dir ++ "/tikz.svg"

  -- Blocks that already open their own @tikzpicture@ (so they can pass picture
  -- options like a 3D basis) are used verbatim; otherwise the block is the
  -- picture body and we wrap it (the established convention — e.g. a bare
  -- pgfplots @axis@).
  let body
        | "\\begin{tikzpicture}" `isInfixOf` tikzCode = tikzCode
        | otherwise = "\\begin{tikzpicture}\n" ++ tikzCode ++ "\n\\end{tikzpicture}"
  writeFile texFile $ tikzPreamble ++ body ++ "\n\\end{document}\n"

  (texCode, texOut, texErr) <- readProcessWithExitCode "lualatex"
    ["-halt-on-error", "-interaction=nonstopmode", "-output-directory=" ++ dir, texFile]
    ""
  case texCode of
    ExitFailure _ -> bail "lualatex" (texOut ++ texErr)
    ExitSuccess -> do
      (svgCode, svgOut, svgErr) <- readProcessWithExitCode "dvisvgm"
        ["--pdf", "--no-fonts", "--output=" ++ svgFile, pdfFile]
        ""
      case svgCode of
        ExitFailure _ -> bail "dvisvgm" (svgOut ++ svgErr)
        ExitSuccess -> do
          svg <- TIO.readFile svgFile          -- strict read before temp dir is cleaned
          return $! Right (T.unpack svg)
  where
    bail tool msg = do
      hPutStrLn stderr $ "[tikz] " ++ tool ++ " failed:\n" ++ msg
      return $ Left (tool ++ " failed (see build log)")

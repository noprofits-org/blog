{-# LANGUAGE OverloadedStrings #-}

-- | Render fenced @tikzpicture@ code blocks to SVG at build time.
--
-- A Markdown code block tagged @.tikzpicture@ is compiled with @pdflatex@
-- and converted to SVG with @pdf2svg@, then embedded as a data-URI @\<img\>@.
-- Posts without any @tikzpicture@ blocks never shell out, so the site builds
-- fine on a machine with no TeX toolchain installed.
module Blog.TikZ
  ( tikzFilter
  , tikzToSvg
  , svgToDataUri
  ) where

import qualified Data.Text as T
import Hakyll (Compiler, unsafeCompiler)
import Text.Pandoc.Definition (Block (..), Format (..))
import qualified Network.URI.Encode as URI
import System.Exit (ExitCode (..))
import System.IO.Temp (withSystemTempDirectory)
import System.Process (readProcessWithExitCode)

-- | Pandoc filter: replace @.tikzpicture@ code blocks with rendered SVG,
-- leaving every other block untouched.
tikzFilter :: Block -> Compiler Block
tikzFilter (CodeBlock (ident, classes, namevals) contents)
  | "tikzpicture" `elem` classes = do
      svg <- unsafeCompiler $ tikzToSvg (T.unpack contents)
      let divAttrs   = (ident, "tikzpicture" : classes, namevals)
          imgElement = RawBlock (Format "html") $ T.pack $
            "<img src=\"" <> svgToDataUri svg
              <> "\" alt=\"TikZ Plot\" style=\"width: 100%; height: auto;\">"
      return $ Div divAttrs [imgElement]
tikzFilter block = return block

-- | Pack a raw SVG string into an inline @data:@ URI (newlines stripped so it
-- is safe to embed in an attribute). Pure, so it is unit-testable.
svgToDataUri :: String -> String
svgToDataUri svg =
  "data:image/svg+xml;utf8," ++ URI.encode (filter (/= '\n') svg)

-- | Compile a TikZ snippet to SVG via @pdflatex@ + @pdf2svg@ in a temp dir.
-- On failure the LaTeX log is printed and the build is aborted.
tikzToSvg :: String -> IO String
tikzToSvg tikzCode = withSystemTempDirectory "hakyll-tikz" $ \tmpDir -> do
  let texFile = tmpDir ++ "/tikz.tex"
      pdfFile = tmpDir ++ "/tikz.pdf"
      svgFile = tmpDir ++ "/tikz.svg"

  writeFile texFile $ unlines
    [ "\\documentclass[crop,tikz]{standalone}"
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
    , "\\begin{tikzpicture}"
    , tikzCode
    , "\\end{tikzpicture}"
    , "\\end{document}"
    ]

  (exitCode, stdout, stderr) <- readProcessWithExitCode "pdflatex"
    ["-halt-on-error", "-file-line-error", "-output-directory=" ++ tmpDir, texFile]
    ""

  case exitCode of
    ExitSuccess -> do
      (exitCode2, stdout2, stderr2) <- readProcessWithExitCode "pdf2svg"
        [pdfFile, svgFile]
        ""
      case exitCode2 of
        ExitSuccess   -> readFile svgFile
        ExitFailure _ -> error $ "pdf2svg failed:\nStdout: " ++ stdout2 ++ "\nStderr: " ++ stderr2
    ExitFailure _ -> do
      putStrLn "pdflatex output:"
      putStrLn stdout
      putStrLn "pdflatex error:"
      putStrLn stderr
      error $ "pdflatex failed with output:\n" ++ stdout ++ "\nError:\n" ++ stderr

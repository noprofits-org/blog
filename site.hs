{-# LANGUAGE BlockArguments      #-}
{-# LANGUAGE ImportQualifiedPost #-}
{-# LANGUAGE LambdaCase         #-}
{-# LANGUAGE NamedFieldPuns     #-}
{-# LANGUAGE OverloadedStrings  #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications   #-}
{-# LANGUAGE ViewPatterns      #-}

import Data.Text qualified as T
import Control.Monad
import Data.List (foldl')
import qualified Data.Map.Strict as Map
import Data.Maybe
import Data.Text (Text)
import Hakyll
import Text.Pandoc.Definition
import Text.Pandoc.Options
import Text.Pandoc.Walk (walk, walkM)
import Debug.Trace
import Text.Pandoc.Extensions (pandocExtensions)
import System.Process (readProcessWithExitCode)
import Data.Hashable (hash)
import qualified Network.URI.Encode as URI
import System.IO.Temp (withSystemTempDirectory)
import System.Exit (ExitCode(..))
import Text.Pandoc.Highlighting (pygments)

-------------------------------------------------------------------------------
main :: IO ()
main = hakyll $ do
    -- Citations
    match "bib/style.csl" $ do
        trace "Compiling CSL..." $ return ()
        compile cslCompiler

    match "bib/bibliography.bib" $ do
        trace "Compiling bibliography..." $ return ()
        compile biblioCompiler

    match "images/*" $ do
        route   idRoute
        compile copyFileCompiler

    match "js/*" $ do
        route   idRoute
        compile copyFileCompiler

    match "css/*" $ do
        route   idRoute
        compile compressCssCompiler

    match (fromList ["about.rst", "contact.markdown", "colophon.markdown"]) $ do
        route   $ setExtension "html"
        compile $ pandocCompiler
            >>= loadAndApplyTemplate "templates/default.html" defaultContext
            >>= relativizeUrls

    match "posts/*" $ do
        route $ setExtension "html"
        compile $ bibtexMathCompiler "bib/style.csl" "bib/bibliography.bib"
            >>= loadAndApplyTemplate "templates/post.html"    postCtx
            >>= loadAndApplyTemplate "templates/default.html" postCtx
            >>= relativizeUrls

    create ["archive.html"] $ do
        route idRoute
        compile $ do
            posts <- recentFirst =<< loadAll "posts/*"
            let archiveCtx =
                    listField "posts" postCtx (return posts) `mappend`
                    constField "title" "Archives"            `mappend`
                    defaultContext

            makeItem ""
                >>= loadAndApplyTemplate "templates/archive.html" archiveCtx
                >>= loadAndApplyTemplate "templates/default.html" archiveCtx
                >>= relativizeUrls

    match "index.html" $ do
        route idRoute
        compile $ do
            posts <- recentFirst =<< loadAll "posts/*"
            let indexCtx =
                    listField "posts" postCtx (return posts) `mappend`
                    constField "title" "Home"                `mappend`
                    defaultContext

            getResourceBody
                >>= applyAsTemplate indexCtx
                >>= loadAndApplyTemplate "templates/default.html" indexCtx
                >>= relativizeUrls

    match "templates/*" $ compile templateCompiler

-------------------------------------------------------------------------------
-- | Process TikZ code blocks
tikzFilter :: Block -> Compiler Block
tikzFilter cb@(CodeBlock (id, classes, namevals) contents)
    | "tikzpicture" `elem` classes = do
        svg <- unsafeCompiler $ tikzToSvg (T.unpack contents)
        let dataUri = "data:image/svg+xml;utf8," ++ URI.encode (filter (/= '\n') svg)
            divAttrs = (id, "tikzpicture":classes, namevals)
            imgElement = RawBlock (Format "html") $ T.pack $ "<img src=\"" <> dataUri <> "\" alt=\"TikZ Plot\" style=\"width: 100%; height: auto;\">"
        return $ Div divAttrs [imgElement]
tikzFilter block = return block

-- | Convert TikZ to SVG using temporary files
tikzToSvg :: String -> IO String
tikzToSvg tikzCode = withSystemTempDirectory "hakyll-tikz" $ \tmpDir -> do
    let texFile = tmpDir ++ "/tikz.tex"
    let pdfFile = tmpDir ++ "/tikz.pdf"
    let svgFile = tmpDir ++ "/tikz.svg"

    -- Write LaTeX file
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

    putStrLn $ "Compiling TeX file at: " ++ texFile
    putStrLn "TeX content:"
    putStrLn =<< readFile texFile

    (exitCode, stdout, stderr) <- readProcessWithExitCode "pdflatex"
        ["-halt-on-error", "-file-line-error", "-output-directory=" ++ tmpDir, texFile]
        ""

    case exitCode of
        ExitSuccess -> do
            putStrLn "pdflatex succeeded"
            (exitCode2, stdout2, stderr2) <- readProcessWithExitCode "pdf2svg"
                [pdfFile, svgFile]
                ""
            case exitCode2 of
                ExitSuccess -> do
                    putStrLn "pdf2svg succeeded"
                    readFile svgFile
                ExitFailure _ -> error $ "pdf2svg failed:\nStdout: " ++ stdout2 ++ "\nStderr: " ++ stderr2
        ExitFailure _ -> do
            putStrLn "pdflatex output:"
            putStrLn stdout
            putStrLn "pdflatex error:"
            putStrLn stderr
            error $ "pdflatex failed with output:\n" ++ stdout ++ "\nError:\n" ++ stderr

bibtexMathCompiler :: String -> String -> Compiler (Item String)
bibtexMathCompiler cslFileName bibFileName = do
    csl <- load $ fromFilePath cslFileName
    bib <- load $ fromFilePath bibFileName

    let mathExtensions = [ Ext_tex_math_dollars
                         , Ext_tex_math_double_backslash
                         , Ext_latex_macros
                         , Ext_raw_tex
                         , Ext_raw_html
                         , Ext_fenced_code_blocks        -- Add these
                         , Ext_backtick_code_blocks      -- code block
                         , Ext_fenced_code_attributes 
                         ]
        defaultExtensions = writerExtensions defaultHakyllWriterOptions
        newExtensions = foldr enableExtension defaultExtensions mathExtensions
        writerOptions = defaultHakyllWriterOptions
            { writerExtensions = newExtensions
            , writerHTMLMathMethod = MathJax ""
            , writerHighlightStyle = Just pygments  -- Add this line
            }
        readerOptions = defaultHakyllReaderOptions
            { readerExtensions = enableExtension Ext_raw_html $
                                 enableExtension Ext_raw_tex pandocExtensions
            }

    getResourceBody
        >>= readPandocBiblio readerOptions csl bib
        >>= \pandoc -> return . writePandocWith writerOptions =<< (walkM tikzFilter =<< return pandoc)

-------------------------------------------------------------------------------
postCtx :: Context String
postCtx =
    dateField "date" "%B %e, %Y" `mappend`
    defaultContext
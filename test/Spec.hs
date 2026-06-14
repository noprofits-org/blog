-- | Minimal test-suite for the pure helpers in the @blog@ library.
-- Kept dependency-light (base only) so it adds no snapshot packages and
-- runs fast in CI.
module Main (main) where

import Blog.TikZ (inlineSvg, namespaceIds)
import Control.Monad (forM_, unless)
import qualified Data.Text as T
import System.Exit (exitFailure)

-- | (name, condition) — each must hold.
checks :: [(String, Bool)]
checks =
  [ ( "inlineSvg strips the XML prolog"
    , inlineSvg "<?xml version=\"1.0\"?>\n<svg>x</svg>" == "<svg>x</svg>"
    )
  , ( "inlineSvg leaves prolog-free markup unchanged"
    , inlineSvg "<svg>y</svg>" == "<svg>y</svg>"
    )
  , ( "inlineSvg passes through input with no <svg> tag"
    , inlineSvg "not an svg" == "not an svg"
    )
  , ( "namespaceIds prefixes a glyph id and its reference identically"
    , namespaceIds (T.pack "n7") (T.pack "<path id='g3-1'/><use xlink:href='#g3-1'/>")
        == T.pack "<path id='n7g3-1'/><use xlink:href='#n7g3-1'/>"
    )
  , ( "namespaceIds prefixes clip-path id and its url() reference"
    , namespaceIds (T.pack "n7") (T.pack "<clipPath id=\"c1\"><g clip-path=\"url(#c1)\">")
        == T.pack "<clipPath id=\"n7c1\"><g clip-path=\"url(#n7c1)\">"
    )
  ]

main :: IO ()
main = do
  let failures = [name | (name, ok) <- checks, not ok]
  forM_ checks $ \(name, ok) ->
    putStrLn $ (if ok then "ok   - " else "FAIL - ") ++ name
  unless (null failures) exitFailure

-- | Minimal test-suite for the pure helpers in the @blog@ library.
-- Kept dependency-light (base only) so it adds no snapshot packages and
-- runs fast in CI.
module Main (main) where

import Blog.TikZ (svgToDataUri)
import Control.Monad (forM_, unless)
import Data.List (isInfixOf, isPrefixOf)
import System.Exit (exitFailure)

-- | (name, condition) — each must hold.
checks :: [(String, Bool)]
checks =
  [ ( "svgToDataUri adds the data-URI prefix"
    , "data:image/svg+xml;utf8," `isPrefixOf` svgToDataUri "<svg></svg>"
    )
  , ( "svgToDataUri strips newlines from the payload"
    , not ("\n" `isInfixOf` svgToDataUri "<svg>\n<rect/>\n</svg>")
    )
  , ( "svgToDataUri percent-encodes angle brackets"
    , "%3C" `isInfixOf` svgToDataUri "<svg/>"
    )
  ]

main :: IO ()
main = do
  let failures = [name | (name, ok) <- checks, not ok]
  forM_ checks $ \(name, ok) ->
    putStrLn $ (if ok then "ok   - " else "FAIL - ") ++ name
  unless (null failures) exitFailure

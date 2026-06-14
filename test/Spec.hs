-- | Minimal test-suite for the pure helpers in the @blog@ library.
-- Kept dependency-light (base only) so it adds no snapshot packages and
-- runs fast in CI.
module Main (main) where

import Blog.TikZ (inlineSvg)
import Control.Monad (forM_, unless)
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
  ]

main :: IO ()
main = do
  let failures = [name | (name, ok) <- checks, not ok]
  forM_ checks $ \(name, ok) ->
    putStrLn $ (if ok then "ok   - " else "FAIL - ") ++ name
  unless (null failures) exitFailure

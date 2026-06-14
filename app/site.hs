-- | Entry point. All rules live in "Blog.Site"; the rest of the build logic
-- (compilers, contexts, feeds, TikZ) lives in the @blog@ library.
module Main (main) where

import Hakyll (hakyll)

import Blog.Site (siteRules)

main :: IO ()
main = hakyll siteRules

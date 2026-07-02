-- | Shared template contexts.
module Blog.Context
  ( postCtx
  ) where

import Hakyll

-- | Context for posts: a human-readable @date@ field plus the defaults.
postCtx :: Context String
postCtx =
  dateField "date" "%B %e, %Y" <>
  defaultContext

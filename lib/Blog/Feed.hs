{-# LANGUAGE OverloadedStrings #-}

-- | Atom/RSS feed configuration and the context the feeds render with.
module Blog.Feed
  ( feedConfiguration
  , feedCtx
  ) where

import Hakyll

import Blog.Context (postCtx)

-- | Shared configuration for both the Atom and RSS feeds.
feedConfiguration :: FeedConfiguration
feedConfiguration = FeedConfiguration
  { feedTitle       = "noprofits.org"
  , feedDescription = "Posts about nonprofits, public-interest data, and the tools behind noprofits.org."
  , feedAuthorName  = "Peter Johnston"
  , feedAuthorEmail = "peter@noprofits.org"
  , feedRoot        = "https://blog.noprofits.org"
  }

-- | Feed entries need a @description@ field, mapped to the post body snapshot.
feedCtx :: Context String
feedCtx = postCtx <> bodyField "description"

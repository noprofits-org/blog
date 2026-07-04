-- | Shared template contexts.
module Blog.Context
  ( postCtx
  ) where

import Data.Char (toLower)
import Data.List (isInfixOf)
import Hakyll

-- | Context for posts: a human-readable @date@ field, the derived @topic@ /
-- @topicSlug@ used by the home-page filter pills, plus the defaults.
--
-- @topic@ is a coarse subject bucket derived from a post's FIRST tag so the
-- Latest filter has a small, stable set of pills instead of one pill per raw
-- tag. The mapping is a plain function (see 'topicBucket') — adjust the keyword
-- table there to re-bucket posts; nothing per-post needs editing.
postCtx :: Context String
postCtx =
  dateField "date" "%B %e, %Y" <>
  topicField "topic"     fst <>
  topicField "topicSlug" snd <>
  tagsHtmlField "tagChips" (\t -> "<span class=\"tag-chip\">" ++ t ++ "</span>") <>
  tagsHtmlField "hashTags" (\t -> "<span class=\"row-tag\">#" ++ t ++ "</span>") <>
  defaultContext

-- | Render each of a post's comma-separated tags to an HTML fragment and
-- concatenate. Empty (field withheld) when a post has no @tags@, so callers can
-- guard with @$if(tagChips)$@. Field output is inserted unescaped by Hakyll —
-- tags are author-controlled plain words, so no escaping is applied.
tagsHtmlField :: String -> (String -> String) -> Context a
tagsHtmlField key render = field key $ \item -> do
  mtags <- getMetadataField (itemIdentifier item) "tags"
  case splitTags mtags of
    []   -> noResult "no tags"
    tags -> pure (concatMap render tags)

-- | Split a raw @tags@ string on commas, trimming whitespace and dropping
-- blanks.
splitTags :: Maybe String -> [String]
splitTags Nothing   = []
splitTags (Just cs) = filter (not . null) (map trim (splitOn ',' cs))
  where
    splitOn c s = case break (== c) s of
      (a, [])     -> [a]
      (a, _ : bs) -> a : splitOn c bs

-- | A field that reads the post's first tag and projects the mapped
-- (label, slug) pair through the given selector.
topicField :: String -> ((String, String) -> String) -> Context a
topicField key sel = field key $ \item -> do
  mtags <- getMetadataField (itemIdentifier item) "tags"
  pure (sel (topicBucket (firstTag mtags)))

-- | The first comma-separated tag, trimmed and lower-cased. Empty when a post
-- has no @tags@ (those fall through to the "Engineering" bucket).
firstTag :: Maybe String -> String
firstTag = maybe "" (trim . map toLower . takeWhile (/= ','))

-- | Map a first tag to a (display label, url slug) subject bucket. Keyword
-- table is scanned in order; first substring hit wins; default is Engineering.
topicBucket :: String -> (String, String)
topicBucket t = go table
  where
    go [] = ("Engineering", "engineering")
    go ((kw, bucket) : rest)
      | kw `isInfixOf` t = bucket
      | otherwise        = go rest
    table =
      [ ("chemis",            ("Chemistry",   "chemistry"))
      , ("spectro",           ("Chemistry",   "chemistry"))
      , ("pigment",           ("Chemistry",   "chemistry"))
      , ("water",             ("Chemistry",   "chemistry"))
      , ("optic",             ("Physics",     "physics"))
      , ("quantum mechanics", ("Physics",     "physics"))
      , ("physics",           ("Physics",     "physics"))
      , ("science",           ("Physics",     "physics"))
      , ("math",              ("Mathematics", "mathematics"))
      , ("nonprofit",         ("Nonprofits",  "nonprofits"))
      , ("non-profit",        ("Nonprofits",  "nonprofits"))
      , ("usaspending",       ("Nonprofits",  "nonprofits"))
      , ("art",               ("Art",         "art"))
      ]

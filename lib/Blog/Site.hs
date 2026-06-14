{-# LANGUAGE OverloadedStrings #-}

-- | The Hakyll rule set for the site, assembled from the library's compilers,
-- contexts, and feed configuration.
module Blog.Site
  ( siteRules
  ) where

import Control.Monad (filterM)
import Hakyll

import Blog.Compilers (bibtexMathCompiler)
import Blog.Context   (postCtx)
import Blog.Feed      (feedConfiguration, feedCtx)

-- | True unless the item's frontmatter sets @draft: true@.
isPublished :: Item a -> Compiler Bool
isPublished item = do
    draft <- getMetadataField (itemIdentifier item) "draft"
    return (draft /= Just "true")

-- | Like 'loadAll', but drops posts marked @draft: true@ from the result.
loadAllPublished :: Pattern -> Compiler [Item String]
loadAllPublished pat = loadAll pat >>= filterM isPublished

-- | Like 'loadAllSnapshots', but drops @draft: true@ posts (used by the feeds).
loadAllPublishedSnapshots :: Pattern -> Snapshot -> Compiler [Item String]
loadAllPublishedSnapshots pat snap = loadAllSnapshots pat snap >>= filterM isPublished

siteRules :: Rules ()
siteRules = do
    -- Citations
    match "bib/style.csl"        $ compile cslCompiler
    match "bib/bibliography.bib" $ compile biblioCompiler

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
            >>= saveSnapshot "content"
            >>= loadAndApplyTemplate "templates/default.html" postCtx
            >>= relativizeUrls

    create ["archive.html"] $ do
        route idRoute
        compile $ do
            posts <- recentFirst =<< loadAllPublished "posts/*"
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
            posts <- recentFirst =<< loadAllPublished "posts/*"
            let indexCtx =
                    listField "posts" postCtx (return posts) `mappend`
                    constField "title" "Home"                `mappend`
                    defaultContext

            getResourceBody
                >>= applyAsTemplate indexCtx
                >>= loadAndApplyTemplate "templates/default.html" indexCtx
                >>= relativizeUrls

    create ["atom.xml"] $ do
        route idRoute
        compile $ do
            posts <- fmap (take 20) . recentFirst
                =<< loadAllPublishedSnapshots "posts/*" "content"
            renderAtom feedConfiguration feedCtx posts

    create ["rss.xml"] $ do
        route idRoute
        compile $ do
            posts <- fmap (take 20) . recentFirst
                =<< loadAllPublishedSnapshots "posts/*" "content"
            renderRss feedConfiguration feedCtx posts

    match "404.html" $ do
        route idRoute
        compile copyFileCompiler

    match "robots.txt" $ do
        route idRoute
        compile copyFileCompiler

    match "templates/*" $ compile templateCompiler

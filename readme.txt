

so far..

app.py has a class categories, genres

-- Categories - movies, tv shows, music, etc (This may be split up further because of the processing differences between them, but at the core they will be
categories (even if categories is a a base inheritance))

-- Genres - Genres are for seperating base categories (rock, jazz, dubstep | horro, comedy, romcom etc)

-- Tags - Tags are for further clustering genres and other things


i REALLY need to make the orm query able to search based off mutiple args, I am trying to make this all from scratch for now (just for 'fun' and suffering)
but I want it to be easily suited to changing over to something like django and sql. That is probably the direction this will need to go into.

but for now I enjoy coding things that I could easily just import :)



update:
  most of the user stuff works (something is wrong with deleting but I have not looked into it), category
  and content loading and saving works.

  I am thinking I may want to make a new db file for each category, because at the moment all the categories
  will be loading and saving to/from one file and that is a huge bottleneck.

  I will need to use data scrapers for getting content genres, tags, and metadata.


  Just because the functionaltity is too great, I will create a cli tool and a web app. At the moment
  everything is just kind of made for cli but I will make the functions take arguments instead of inputs, and
  that will just be taken care of in the different deployments of the base app.

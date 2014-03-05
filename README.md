SSUNS 2014
==========

Built with Django.
=======


* [Usage information](#usage-information)
    * [Disclaimer](#disclaimer)
    * [Setting it up](#setting-it-up)
    * [Editing content](#editing-content)
        * [Types of pages](#types-of-pages)
        * [Adding/editing a page](#adding-editing-a-page)
        * [Uploading media](#uploading-media)
    * [Editing the design](#editing-the-design)
        * [Images](#images)
        * [Stylesheets](#stylesheets)
    * [Editing functionality](#editing-functionality)
    * [Other information](#other-information)
* [Licensing information](#licensing-information)
* [Contact information](#contact-information)


Usage information
-----------------

### Disclaimer

If you want to use this codebase for your own website, keep in mind that the
site was built for a very specific purpose (i.e., McMUN/SSUNS 2014), and thus
there may be issues with adapting it for other purposes. There is also some
hastily tacked-on code that I couldn't avoid, which I'm not too proud of.
I cannot be held responsible for any issues (e.g., data loss, weight loss,
hair loss) that may arise from the usage of this codebase.

### Setting it up

You'll need to install a bunch of dependencies, preferrably with pip:
Django, Markdown, celery, xhtml2pdf, fabric, maybe some others. I'll create
a requirements.txt file for this later. For development, using SQLite should
be fine, so just run `python manage.py syncdb` and create the superuser.
Then, to run the development server locally at port 8000, run `fab up` (or
`python manage.py runserver` if you don't have Fabric installed or just like
typing). You will then be able to access the website at
<http://localhost:8000>.

For production, you'll want to edit the database settings in
mcmun/settings.py, and you probably don't want to use the development
server. [Gunicorn](http://gunicorn.org/) is a good choice. You can serve
static content using nginx or Apache or whatever web server you're using.

### Editing content

There is a homegrown content management system application installed. It
provides a web interface for managing the menu as well as the content of the
pages showing up in the menu. It's fairly rudimentary, so you can't do
anything complicated like form processing or user customisation (see the
[Editing functionality](#editing-functionality) section below for info on
that). However, it does make managing content much easier.

To use it, first log in to the admin panel (www.example.com/admin/) using
the superuser account details, and click on 'Cms'.

#### Types of pages

Do you want the page to show up as a top-level link in the menu bar? You
want to add a parent page. Click 'Add' next to 'Parent pages'. Do you want
it to show up under a particular top-level link in the menu bar? You want to
add a subpage. Click 'Add' next to 'Sub pages', and choose the desired
top-level link you want it to be under to be the 'Parent'.

#### Adding/editing a page

The short name is the slug (what will show up in the URL when you're at the
page), the long name is the title that will show up in the browser titlebar
(and on the page as well if "Show nav" is checked). The content is what will
show up on the page in the white section. It's processed with
[Markdown](http://daringfireball.net/projects/markdown/), and HTML is
enabled.

If you need to do something very HTML-intensive, it might be nicer
to use an actual HTML template (so you can use your own editor and keep it
under version control). In this case, you'll want to check the 'Custom
template' box. The HTML file must be placed in the following directory:
`cms/templates/pages`, and it must be named `{short name}.html` where
`{short name}` is the actual short name.

The 'Position' field should hold an integer determining the position of the
page relative to the other pages of the same type. So if you have pages A,
B, and C, and you want them to show up in that order, then A should be 1, B
should be 2, C should be 3 (or something like that). If A is a parent page
with children B and C, and D is the next parent page (immediately to the
right of A) with children E and F, then the positions should be: A=1, B=1,
C=2, D=2, E=1, F=1.  (This system is a bit unwieldy - it's on my list of
things to fix.)

### Uploading media

Unfortunately there is no web interface for uploading images and other
media. For now, you'll have to upload them to the server using SCP or SFTP
or whatever. I usually place images files in `static/img/` and
other documents in `static/files/`. These files can then be accessed
under /static/img/ and /static/files/ respectively (relative to
the root of your website).

### Editing the design

#### Images

As mentioned previously, all the images are located in `static/img/`.

#### Stylesheets

For stylesheets, I use [LESS](http://lesscss.org), which is a superset of
CSS that provides awesome things like variables, operations, and nesting.
The stylesheet definitions can be found in `static/css/`.
`mcmun.css` is the compiled CSS file that is actually served to the user.
Since this is automatically generated by the LESS compiler, you won't want
to edit this file. Instead, you'll have to edit the `*.less` files:

* `fonts.less`: Font-embedding for the
  [Raleway](http://www.theleagueofmoveabletype.com/raleway) font (used in
  headers) with `@font-face`, as well as the two font-definitions that are
  used (`#raleway` and `#sans-serif`). All the font files can be found under
  the `fonts/` subdirectory.
* `forms.less`: Some basic form styling.
* `menu.less`: The menu styling is defined here. It's a pure CSS
  implementation (i.e., no Javascript) using lists, so most of the
  layout-based definitions in this file are necessary, if somewhat obtuse.
  Be careful when changing anything in this file.
* `mixins.less`: Various mixins are defined here: gradients, vendor
  prefixes, layout, transparency, etc.
* `variables.less`: All the variables are defined here. If you want to change
  a colour definition, this is probably the best place to look.
* `mcmun.less`: The rest of the site-specific styles are defined here.

To make your changes visible on the website, you'll need to use the
[LESS](http://lesscss.org/) compiler. This can be installed through the node
package managing system with `npm install -g less` (the package manager can
itself be installed through apt-get or whatever your operating system's
package manager is).  Once this is installed, you'll be able to compile any
changes you make to the source by running `fab less` (see `fabfile.py` if
Fabric is not installed for the full command).

### Editing functionality

In Django, functionality is implemented on the **application** level. The
following applications are included:

* `cms`: The content management system, for controlling the content of
  pages.
* `committees`: Everything committee-related, including committee
  applications and delegation assignments.
* `mcmun`: Everything registration-related that is not also
  committee-related. This includes school information, invoice generation,
  and scholarship applications.

To learn more about how Django applications work, it may be a good idea to
read the [tutorial](https://docs.djangoproject.com/en/dev/intro/tutorial01/)
on writing apps. After that, the .py files within each application
subdirectory are recommended reading, and should be fairly self-explanatory.

More documentation on this will be available soon.

### Other information

This readme will be updated with more information as I think of it. Contact
it@ssuns.org or it@mcmun.org if you have any questions.

Licensing information
---------------------

This repository isn't licensed under any of the standard OSI-approved
licenses because I couldn't really find one that fit. In non-legal terms:
feel free to use any Python/JS/LESS snippets you see. Attribution is not
required. Please don't use the content, however. Please also refrain from
copying the design wholesale. That would make me sad.

Source information for the images:

* "I mean, I'm not making any money from this, so that counts as
  non-commercial usage, right?") and I guess I'll release the derivative
  under the same license because why not.  The bridge photo on the homepage,
  the photo of Montreal on the "About Montreal" page and the photo of McGill
  on the "About McGill" page are all public domain. The originals can be
  found on the Wikimedia Commons page for Montreal/McGill.
* The photos on the "Contact us" and "Meet the secretariat" pages are,
  pretty obviously, photos of secretariat members.
* The photos in the Registration/Welcome/Committees block on the home page
  were taken by either a secretariat member or someone related to SSUNS in
  some way.  The rest of the images - the dove, the logo, the contact icons
  in the header - I created in Inkscape. They're not available under any
  sort of copyleft license, unfortunately. Using the logo for illustration
  purposes in the context of McMUN/SSUNS is, of course, totally fine.

Contact information
-------------------

Email: <it@ssuns.org>

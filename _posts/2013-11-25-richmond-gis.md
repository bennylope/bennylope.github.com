---
published: true
title: "Freeing Public City Data: Making Richmond's GIS data accessible"
layout: post
permalink: /2013/richmond-gis-data/
soHelpful: true
comments: true
---

The City of Richmond makes a lot of its data publicly accessible, I'm
told, in an effort to encourge "civic hacking". I'm not yet sure where
all of this data is - there's no data clearinghouse that I'm aware of - but the
city does publish some of the standard data you'd expect. Real estate
parcels, voting precincts, police crime reports, etc. And like many of
the government provided data sets in the past the city's data sets
reflect prioritizing public access over public accessibility.

### Data interfaces

You can look up information about [city real
estate](http://eservices.ci.richmond.va.us/applications/PropertySearch/),
including assessments and transaction histories, but on a parcel by parcel basis.
You'll need either a street address or a parcel identifier.  You can
look through [police crime
reports](http://eservices.ci.richmond.va.us/applications/crimeinfo/index.asp),
too, although you need to do so by selecting a top level category like
neighborhood or precinct and then filtering down. Here's what that
interface looks like.

![Richmond City police department
statistics](/images/rva-police-data.png)

And here's a snapshot of the crime statistics in my neighborhood after
selecting statistics by neighborhood for the last month.

![Carytown crime stats](/images/rva-carytown-crime.png)

You can download the detailed data for an individual category's crime
statistics for the given time period, but you're restricted to doing so
for that category (e.g. neighborhood) and time period. There's no
apparent pan-category data dump. So to get this data out you need to
write a spider to get the data for you. And of course the data must be
requested through a single endpoint by HTTP POST with the requisite
cookies set.

As for the real estate data, there is no such way to download the city's
real estate data, although you can purchase the public data set for
$100. I'm planning on requesting the entire set.

Paid or not, there are no APIs that I've been able to find.

### Maps and data formats

The city makes its GIS data available available however via [an FTP site](ftp://ftp.ci.richmond.va.us/GIS/).
This sounds absolutely quaint until you realize how simple it is
and completely superior than our options for pretty much every other
data set. 

For statistical data it's pretty common to find this offered in one or
more types of Microsoft Office formats and then a text format. At least
with a text file you can usually read it into any program of your choice
for storage or analysis.

With the city's geographic data, this is all offered in ESRI shapefiles.
This is a standard GIS format and in many ways it makes perfect sense to
offer the data directly in this format. It doesn't require any
conversion (i.e. extra work) and most of the professionals who might be
using this data will be using GIS software compatible with shapefiles.
Most "civic hackers" probably won't be though. And for my immediate purposes I'm
more interested in being able to view and share the map data. So a
format like GeoJSON makes a lot more sense. We just need to convert the
files.

### Shapefiles to GeoJSON

First download the data from the source. In this case the Richmond GIS
office provides their files via the city's [FTP site](ftp://ftp.ci.richmond.va.us/GIS/). I used my [go-to FTP
client](https://www.panic.com/transmit/)
to sync the GIS folder to a local folder and walked away. Having
downlaoded the data I was left with a file structure including numerous
zip files containing the shapefiles I was after. The proper way to get
at these would be to script the entire process of unzipping and
conversion. What I wanted to do was extract each file in place, and
given my still limited shell-fu this turned out to be quicker to simply
unzip theme one by one and then run the conversion.

With the unzipped data files safely in hand it's time to convert the the
shapefiles to GeoJSON format. To do so I used
[`ogr2ogr`](http://www.gdal.org/ogr2ogr.html) which should be available
if you have [`gdal`](http://www.gdal.org/) installed. On a Mac you can
install this with Homebrew:

    brew install gdal

Now all we need to do is specify the output format and the projection to
produce the requisite GeoJSON files. This was a bit simpler to do in the
shell. This command finds every shapefile and pipes that filename to
`ogr2ogr` using `xargs`.

    find . -name "*.shp" -print0 | xargs -0 -I {} ogr2ogr -f GeoJSON -t_srs crs:84 {}.geojson {}

The `ogr2ogr` arguments specify the output format and the coordinate system.
[crs:84](http://mapserver.org/ogc/wms_server.html#coordinate-systems-and-axis-orientation)
specifies that the output coordinate system should use
the [WGS 84 system](http://wiki.gis.com/wiki/index.php/WGS84). As this
is the only one that [GitHub's rendering
system](https://help.github.com/articles/mapping-geojson-files-on-github#troubleshooting)
supports you should specify it here.

I've not
done anything to amend the filenames except for appending the new
`geojson` extension. This is primarily for simplicity of execution but
also makes very explicit that this was converted from the named
shapefile.

Some of the output files end up being pretty damn big. What the
shapefile format lacks in accessibility it makes up for in size. I
excluded all large files over 50 MB from the repository. Large files
can make Git repos slow to work with, and as I wanted to host this on
GitHub 100 MB files are verbotten. The 1 GB countour file was
out of the question. These were all gzipped and shared publicly via an
S3 bucket.

<script src="https://embed.github.com/view/geojson/bennylope/Richmond-GIS/master/Landmarks/VotingStations.shp.geojson?height=400&amp;width=700">&nbsp;</script>

You can access the remainder of the files in the [Richmond GIS
repository](https://github.com/bennylope/Richmond-GIS/).

### Next steps

I've started going through some of the larger GeoJSON files and
transforming them into
[TopoJSON](https://github.com/mbostock/topojson/wiki) files. This is a
related JSON format that simplifies the data by deduping lines, at least
for the purpose of representing topology. E.g. instead of city council
districts being represented as individual polygons, with overlaping
edges, those edges are reduced to a single edge (arcs). As important, the
`topojson` tool also has some features for [simplifying the
arcs](http://bost.ocks.org/mike/simplify/). A small reduction in
resolution can yield large reductions in map size with little to no
effect on our perception of or the utility of the map.

It's worth reiterating some reasonable expectations when dealing with
government data, especially local government data. You're not going to
get the interface you want and you're not going to get the dataformats
you want. You just have to accept that to start. That's not to say that
you shouldn't ask, or better yet offer to help your local government
identify and produce data in a way that's accessible, but don't expect
it to work that way. Be prepared to work with data in a
format that makes sense for the providing office, not necessarily for
citizens or other interested third-parties.

I took some cues from Ben Balter's [blog post on converting
shapefiles](http://ben.balter.com/2013/06/26/how-to-convert-shapefiles-to-geojson-for-use-on-github/)
and recommend checking out his write up.

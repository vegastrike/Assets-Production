PH01 COCKPIT.
made by Paul Heldens with Gimp.

# unpack
tar -jxvf ph01_cockpit*.tar.bz2
cd ph01_cockpit*

# backup existing
mv ./cockpits/disabled-cockpit.cpt $VSDATADIR/cockpits/disabled-cockpit.cpt_bak

# install new
cp -r ./cockpits/disabled-cockpit.cpt $VSDATADIR/cockpits/
cp -r ./textures/ph01_cockpit $VSDATADIR/textures/

#recommended ~/.vegastrike/vegastrike.config settings:
<var name="high_quality_sprites" value="true" />
# required ~/.vegastrike/vegastrike.config settings:
<var name="blend_panels" value="true"/>
<var name="draw_rendered_crosshairs" value="false" />

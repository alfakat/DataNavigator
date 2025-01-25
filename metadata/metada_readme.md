 **Metadata** is data providing information about data.
 
Each type of data comes with metadata and different types of metadata come 
with their important for further processing information. 

For instance, metadata of image is:
- resolution;
- extension;
- bitrate;
- encoding;
- creation date.

Depends on data collection method, metadata can include:
- device, megapixels, focal lenght for recording images;
- source, alternative text, style for scrapped images;
- prompt, seed, steps parameters for generated images;

There is at least one common metadata for all images - its resolution.

Metadata can be stored in different formats such as json, csv or hdf5 as transit step before inserting 
into database.
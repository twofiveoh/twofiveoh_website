module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("./src/css");
    eleventyConfig.addPassthroughCopy("./src/img");
    
    eleventyConfig.addCollection('episodesorted', function(collectionApi) {
      return collectionApi.getFilteredByTag("episode")
          .sort((a, b) => b.data.epindex - a.data.epindex).reverse();
   });

  return {
    // pathPrefix: "/twofiveoh_website/",
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};
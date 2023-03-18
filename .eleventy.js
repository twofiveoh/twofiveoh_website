module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("./src/css");
    eleventyConfig.addPassthroughCopy("./src/img");
    
  return {
    // pathPrefix: "/twofiveoh_website/",
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};
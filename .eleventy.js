module.exports = function (eleventyConfig) {
  return {
    pathPrefix: "/twofiveoh_website/",
    dir: {
      input: "src",
      output: "public",
      includes: "_includes",
    },
  };
};
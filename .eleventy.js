const htmlmin = require("html-minifier");
const rimraf = require("rimraf");

module.exports = function (eleventyConfig) {
  // delete contents of public to ensure removed files are removed from the final build
  rimraf.windows.sync("public/");

  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/img");

  // sort episodes by index
  eleventyConfig.addCollection('episodesorted', function (collectionApi) {
    return collectionApi.getFilteredByTag("episode")
      .sort((a, b) => b.data.epindex - a.data.epindex).reverse();
  });

  // minify all html files
  eleventyConfig.addTransform("htmlmin", function (content) {
    if (this.page.outputPath && this.page.outputPath.endsWith(".html")) {
      let minified = htmlmin.minify(content, {
        useShortDoctype: true,
        removeComments: true,
        collapseWhitespace: true
      });
      return minified;
    }
    return content;
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
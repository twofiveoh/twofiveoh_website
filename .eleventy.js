const htmlmin = require("html-minifier");
const rimraf = require("rimraf");
const cleancss = require("clean-css");

module.exports = function (eleventyConfig) {
  // delete contents of public to ensure removed files are removed from the final build
  rimraf.windows.sync("public/");

  eleventyConfig.addPassthroughCopy("./src/css");
  eleventyConfig.addPassthroughCopy("./src/img");

  // sort episodes by index
  eleventyConfig.addCollection('episodesorted', function (collectionApi) {
    return collectionApi.getFilteredByTag("episode")
      .sort((a, b) => parseFloat(b.data.epindex) - parseFloat(a.data.epindex)).reverse();
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
  
  // clean and inline all css files
  eleventyConfig.addFilter("cssmin", function(code) {
    return new cleancss({}).minify(code).styles;
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

//
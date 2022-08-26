process.traceDeprecation = true;
const path = require("path");
const package_json = require("./package.json");
const package_json_mockup = require("@plone/mockup/package.json");
const package_json_patternslib = require("@patternslib/patternslib/package.json");
const webpack_config = require("@patternslib/dev/webpack/webpack.config").config;
const mf_config = require("@patternslib/dev/webpack/webpack.mf");

module.exports = () => {
    let config = {
        entry: {
            "imagecropping.min": path.resolve(__dirname, "resources/index"),
        },
    };

    config = webpack_config({
        config: config,
        package_json: package_json,
    });
    config.output.path = path.resolve(
        __dirname,
        "src/plone/app/imagecropping/browser/static"
    );

    config.plugins.push(
        mf_config({
            name: "plone-imagecropping",
            filename: "imagecropping-remote.min.js",
            remote_entry: config.entry["imagecropping.min"],
            dependencies: {
                ...package_json_patternslib.dependencies,
                ...package_json_mockup.dependencies,
                ...package_json.dependencies,
            },
        })
    );

    if (process.env.NODE_ENV === "development") {
        config.devServer.port = "8011";
        config.devServer.static.directory = __dirname;
    }

    return config;
};

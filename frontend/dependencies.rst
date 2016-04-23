This document covers modules installed via npm that are used for building the frontend.

Required for build
------------------

webpack requirements/plugins/loaders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **babel** Transpiler for es6-7 to es5 (may be able to ignore transpiling if targeting modern browsers such as Chromium on the pi)
* **babel-core**
* **babel-eslint**
* **babel-loader** Webpack loader for babel files
* **babel-preset-es2015**
* **babel-preset-react**
* **babel-preset-stage-0**
* **compression-webpack-plugin**
* **json-loader**
* **react-hot-loader**
* **webpack**
* **webpack-bundle-tracker** For use with django-webpack
* **webpack-hot-middleware**

Extras
~~~~~~

* **chalk** Console colors!

Frontend dependencies
~~~~~~~~~~~~~~~~~~~~~

* **react**
* **react-dom**
* **react-relay**
* **react-hot-loader**

Testing dependencies
~~~~~~~~~~~~~~~~~~~~

TODO
----

* Pull in a testing tool and integrate it into dev build

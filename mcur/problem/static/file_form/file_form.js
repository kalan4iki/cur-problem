!function(e){var t={};function r(n){if(t[n])return t[n].exports;var o=t[n]={i:n,l:!1,exports:{}};return e[n].call(o.exports,o,o.exports,r),o.l=!0,o.exports}r.m=e,r.c=t,r.d=function(e,t,n){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},r.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)r.d(n,o,function(t){return e[t]}.bind(null,o));return n},r.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="",r(r.s=5)}([function(e,t){var r;r=function(){return this}();try{r=r||new Function("return this")()}catch(e){"object"==typeof window&&(r=window)}e.exports=r},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});t.default=function(){return"undefined"!=typeof navigator&&"string"==typeof navigator.product&&"reactnative"===navigator.product.toLowerCase()}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=function(){function e(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}return function(t,r,n){return r&&e(t.prototype,r),n&&e(t,n),t}}();t.getStorage=function(){return o?new a:null};var o=!1;try{o="localStorage"in window;var i="tusSupport";localStorage.setItem(i,localStorage.getItem(i))}catch(e){if(e.code!==e.SECURITY_ERR&&e.code!==e.QUOTA_EXCEEDED_ERR)throw e;o=!1}t.canStoreURLs=o;var a=function(){function e(){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e)}return n(e,[{key:"setItem",value:function(e,t,r){r(null,localStorage.setItem(e,t))}},{key:"getItem",value:function(e,t){t(null,localStorage.getItem(e))}},{key:"removeItem",value:function(e,t){t(null,localStorage.removeItem(e))}}]),e}()},function(e,t,r){"use strict";var n,o=r(7),i=(n=o)&&n.__esModule?n:{default:n},a=function(e){if(e&&e.__esModule)return e;var t={};if(null!=e)for(var r in e)Object.prototype.hasOwnProperty.call(e,r)&&(t[r]=e[r]);return t.default=e,t}(r(2));var s=i.default.defaultOptions,u={Upload:i.default,canStoreURLs:a.canStoreURLs,defaultOptions:s};if("undefined"!=typeof window){var l=window,f=l.XMLHttpRequest,c=l.Blob;u.isSupported=f&&c&&"function"==typeof c.prototype.slice}else u.isSupported=!0,u.FileStorage=a.FileStorage;e.exports=u},function(e,t,r){"use strict";
/*!
 * escape-html
 * Copyright(c) 2012-2013 TJ Holowaychuk
 * Copyright(c) 2015 Andreas Lubbe
 * Copyright(c) 2015 Tiancheng "Timothy" Gu
 * MIT Licensed
 */var n=/["'&<>]/;e.exports=function(e){var t,r=""+e,o=n.exec(r);if(!o)return r;var i="",a=0,s=0;for(a=o.index;a<r.length;a++){switch(r.charCodeAt(a)){case 34:t="&quot;";break;case 38:t="&amp;";break;case 39:t="&#39;";break;case 60:t="&lt;";break;case 62:t="&gt;";break;default:continue}s!==a&&(i+=r.substring(s,a)),s=a+1,i+=t}return s!==a?i+r.substring(s,a):i}},function(e,t,r){e.exports=r(6)},function(e,t,r){"use strict";r.r(t),function(e){var t=r(3),n=r(4),o=r.n(n);function i(e){return function(e){if(Array.isArray(e)){for(var t=0,r=new Array(e.length);t<e.length;t++)r[t]=e[t];return r}}(e)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance")}()}function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function s(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function u(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function l(e,t,r){return t&&u(e.prototype,t),r&&u(e,r),e}var f=function(){function e(t){var r=t.container,n=t.input,o=t.skipRequired,i=t.translations;s(this,e),this.container=r,this.input=n,this.translations=i,this.filesContainer=this.createFilesContainer(),o&&(this.input.required=!1)}return l(e,[{key:"createFilesContainer",value:function(){var e=document.createElement("div");return e.className="dff-files",this.container.appendChild(e),e}},{key:"addUploadedFile",value:function(e,t){this.addFile(e,t),this.setSuccess(t)}},{key:"addNewUpload",value:function(e,t){var r=this.addFile(e,t),n=document.createElement("span");n.className="dff-progress";var o=document.createElement("span");o.className="dff-progress-inner",n.appendChild(o),r.appendChild(n);var i=document.createElement("a");i.className="dff-cancel",i.innerHTML=this.translations.Cancel,i.setAttribute("data-index",t),i.href="#",r.appendChild(i)}},{key:"addFile",value:function(e,t){var r=document.createElement("div");r.className="dff-file-id-".concat(t);var n=document.createElement("span");return n.innerHTML=o()(e),r.appendChild(n),this.filesContainer.appendChild(r),this.input.required=!1,r}},{key:"deleteFile",value:function(e){var t=this.findFileDiv(e);t&&t.remove()}},{key:"setError",value:function(e){var t=document.createElement("span");t.classList.add("dff-error"),t.innerHTML=this.translations["Upload failed"];var r=this.findFileDiv(e);r.appendChild(t),r.classList.add("dff-upload-fail"),this.removeProgress(e),this.removeCancel(e)}},{key:"setDeleteFailed",value:function(e){var t=this.findFileDiv(e),r=document.createElement("span");r.innerHTML=this.translations["Delete failed"],t.appendChild(r)}},{key:"findFileDiv",value:function(e){return this.filesContainer.querySelector(".dff-file-id-".concat(e))}},{key:"setSuccess",value:function(e){var t=this.translations,r=this.findFileDiv(e);r.classList.add("dff-upload-success");var n=document.createElement("a");n.innerHTML=t.Delete,n.className="dff-delete",n.setAttribute("data-index",e),n.href="#",r.appendChild(n),this.removeProgress(e),this.removeCancel(e)}},{key:"removeProgress",value:function(e){var t=this.findFileDiv(e).querySelector(".dff-progress");t&&t.remove()}},{key:"removeCancel",value:function(e){var t=this.findFileDiv(e).querySelector(".dff-cancel");t&&t.remove()}},{key:"clearInput",value:function(){this.input.value=""}},{key:"updateProgress",value:function(e,t){var r=this.filesContainer.querySelector(".dff-file-id-".concat(e)).querySelector(".dff-progress-inner");r&&(r.style.width="".concat(t,"%"))}}]),e}(),c=function(){function e(r){var n=this,o=r.input,u=r.container,l=r.fieldName,c=r.formId,d=r.initial,p=r.multiple,h=r.skipRequired,_=r.translations,v=r.uploadUrl;s(this,e),a(this,"onChange",(function(e){var r=i(e.target.files);0!==r.length&&(n.multiple||0===n.uploads.length||(n.renderer.deleteFile(0),n.uploads=[]),r.forEach((function(e){var r=n.fieldName,o=n.formId,i=n.renderer,a=n.uploads,s=n.uploadUrl,u=e.name,l=a.length,f=new t.Upload(e,{endpoint:s,metadata:{fieldName:r,filename:u,formId:o},onError:function(){return n.handleError(l)},onProgress:function(e,t){return n.handleProgress(l,e,t)},onSuccess:function(){return n.handleSuccess(l)}});f.start(),i.addNewUpload(u,l),n.uploads.push(f)})))})),a(this,"onClick",(function(e){var t=e.target;if(t.classList.contains("dff-delete")){var r=parseInt(t.getAttribute("data-index"),10);n.handleDelete(r)}else if(t.classList.contains("dff-cancel")){var o=parseInt(t.getAttribute("data-index"),10);n.handleCancel(o)}})),a(this,"handleProgress",(function(e,t,r){var o=(t/r*100).toFixed(2);n.renderer.updateProgress(e,o)})),a(this,"handleError",(function(e){n.renderer.setError(e)})),a(this,"handleSuccess",(function(e){var t=n.renderer;t.clearInput(),t.setSuccess(e)})),this.fieldName=l,this.formId=c,this.multiple=p,this.uploadUrl=v,this.uploadIndex=0,this.uploads=[],this.renderer=new f({container:u,input:o,skipRequired:h,translations:_}),d&&this.addInitialFiles(d),o.addEventListener("change",this.onChange),u.addEventListener("click",this.onClick)}return l(e,[{key:"addInitialFiles",value:function(e){var t=this;if(0!==e.length){var r=this.multiple,n=this.renderer,o=function(e,r){n.addUploadedFile(e.name,r),t.uploads.push({url:"".concat(t.uploadUrl).concat(e.id)})};if(r){var i=0;e.forEach((function(e){o(e,i),i+=1}))}else o(e[0],0)}}},{key:"handleDelete",value:function(e){var t=this,r=this.uploads[e].url,n=new window.XMLHttpRequest;n.open("DELETE",r),n.onload=function(){204===n.status?t.renderer.deleteFile(e):t.renderer.setDeleteFailed(e)},n.setRequestHeader("Tus-Resumable","1.0.0"),n.send(null)}},{key:"handleCancel",value:function(e){this.uploads[e].abort(!0),this.renderer.deleteFile(e)}}]),e}();e.initUploadFields=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},r=function(e){return t&&t.prefix?"".concat(t.prefix,"-").concat(e):e},n=function(t){var n=r(t),o=e.querySelector('[name="'.concat(n,'"]'));return o?o.value:(console.error("Cannot find input with name '".concat(n,"'")),null)},o=function(e){var t=e.dataset.files;return t?JSON.parse(t):[]},i=n("upload_url"),a=n("form_id"),s=t.skipRequired||!1;a&&i&&e.querySelectorAll(".dff-uploader").forEach((function(e){var t=e.querySelector(".dff-container");if(t){var r=t.querySelector("input[type=file]");if(r){var n=r.name,u=r.multiple,l=o(t),f=JSON.parse(t.getAttribute("data-translations"));new c({container:e,fieldName:n,formId:a,initial:l,input:r,multiple:u,skipRequired:s,translations:f,uploadUrl:i})}}}))}}.call(this,r(0))},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=function(){function e(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}return function(t,r,n){return r&&e(t.prototype,r),n&&e(t,n),t}}(),o=f(r(8)),i=f(r(9)),a=r(10),s=r(11),u=r(15),l=r(2);function f(e){return e&&e.__esModule?e:{default:e}}var c={endpoint:null,fingerprint:f(r(19)).default,resume:!0,onProgress:null,onChunkComplete:null,onSuccess:null,onError:null,headers:{},chunkSize:1/0,withCredentials:!1,uploadUrl:null,uploadSize:null,overridePatchMethod:!1,retryDelays:null,removeFingerprintOnSuccess:!1,uploadLengthDeferred:!1,urlStorage:null,fileReader:null,uploadDataDuringCreation:!1},d=function(){function e(t,r){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.options=(0,i.default)(!0,{},c,r),this._storage=this.options.urlStorage,this.file=t,this.url=null,this._xhr=null,this._fingerprint=null,this._offset=null,this._aborted=!1,this._size=null,this._source=null,this._retryAttempt=0,this._retryTimeout=null,this._offsetBeforeRetry=0}return n(e,[{key:"start",value:function(){var e=this,t=this.file;t?this.options.endpoint||this.options.uploadUrl?(this.options.resume&&null==this._storage&&(this._storage=(0,l.getStorage)()),this._source?this._start(this._source):(this.options.fileReader||u.getSource)(t,this.options.chunkSize,(function(t,r){t?e._emitError(t):(e._source=r,e._start(r))}))):this._emitError(new Error("tus: neither an endpoint or an upload URL is provided")):this._emitError(new Error("tus: no file or stream to upload provided"))}},{key:"_start",value:function(e){var t=this,r=this.file;if(this.options.uploadLengthDeferred)this._size=null;else if(null!=this.options.uploadSize){if(this._size=+this.options.uploadSize,isNaN(this._size))return void this._emitError(new Error("tus: cannot convert `uploadSize` option into a number"))}else if(this._size=e.size,null==this._size)return void this._emitError(new Error("tus: cannot automatically derive upload's size from input and must be specified manually using the `uploadSize` option"));var n=this.options.retryDelays;if(null!=n){if("[object Array]"!==Object.prototype.toString.call(n))return void this._emitError(new Error("tus: the `retryDelays` option must either be an array or null"));var o=this.options.onError;this.options.onError=function(e){t.options.onError=o,null!=t._offset&&t._offset>t._offsetBeforeRetry&&(t._retryAttempt=0);var r=!0;"undefined"!=typeof window&&"navigator"in window&&!1===window.navigator.onLine&&(r=!1);var i=e.originalRequest?e.originalRequest.status:0,a=!p(i,400)||409===i||423===i;if(t._retryAttempt<n.length&&null!=e.originalRequest&&a&&r){var s=n[t._retryAttempt++];t._offsetBeforeRetry=t._offset,t.options.uploadUrl=t.url,t._retryTimeout=setTimeout((function(){t.start()}),s)}else t._emitError(e)}}if(this._aborted=!1,null==this.url)return null!=this.options.uploadUrl?(this.url=this.options.uploadUrl,void this._resumeUpload()):void(this._hasStorage()?this.options.fingerprint(r,this.options,(function(e,r){e?t._emitError(e):(t._fingerprint=r,t._storage.getItem(t._fingerprint,(function(e,r){e?t._emitError(e):null!=r?(t.url=r,t._resumeUpload()):t._createUpload()})))})):this._createUpload());this._resumeUpload()}},{key:"abort",value:function(t,r){var n=this;null!==this._xhr&&(this._xhr.abort(),this._source.close()),this._aborted=!0,null!=this._retryTimeout&&(clearTimeout(this._retryTimeout),this._retryTimeout=null),r=r||function(){},t?e.terminate(this.url,this.options,(function(e,t){if(e)return r(e,t);n._hasStorage()?n._storage.removeItem(n._fingerprint,r):r()})):r()}},{key:"_hasStorage",value:function(){return this.options.resume&&this._storage}},{key:"_emitXhrError",value:function(e,t,r){this._emitError(new o.default(t,r,e))}},{key:"_emitError",value:function(e){if("function"!=typeof this.options.onError)throw e;this.options.onError(e)}},{key:"_emitSuccess",value:function(){"function"==typeof this.options.onSuccess&&this.options.onSuccess()}},{key:"_emitProgress",value:function(e,t){"function"==typeof this.options.onProgress&&this.options.onProgress(e,t)}},{key:"_emitChunkComplete",value:function(e,t,r){"function"==typeof this.options.onChunkComplete&&this.options.onChunkComplete(e,t,r)}},{key:"_setupXHR",value:function(e){this._xhr=e,h(e,this.options)}},{key:"_createUpload",value:function(){var e=this;if(this.options.endpoint){var t=(0,s.newRequest)();t.open("POST",this.options.endpoint,!0),t.onload=function(){if(p(t.status,200)){var r=t.getResponseHeader("Location");if(null!=r){if(e.url=(0,s.resolveUrl)(e.options.endpoint,r),0===e._size)return e._emitSuccess(),void e._source.close();e._hasStorage()&&e._storage.setItem(e._fingerprint,e.url,(function(t){t&&e._emitError(t)})),e.options.uploadDataDuringCreation?e._handleUploadResponse(t):(e._offset=0,e._startUpload())}else e._emitXhrError(t,new Error("tus: invalid or missing Location header"))}else e._emitXhrError(t,new Error("tus: unexpected response while creating upload"))},t.onerror=function(r){e._emitXhrError(t,new Error("tus: failed to create upload"),r)},this._setupXHR(t),this.options.uploadLengthDeferred?t.setRequestHeader("Upload-Defer-Length",1):t.setRequestHeader("Upload-Length",this._size);var r=function(e){var t=[];for(var r in e)t.push(r+" "+a.Base64.encode(e[r]));return t.join(",")}(this.options.metadata);""!==r&&t.setRequestHeader("Upload-Metadata",r),this.options.uploadDataDuringCreation&&!this.options.uploadLengthDeferred?(this._offset=0,this._addChunkToRequest(t)):t.send(null)}else this._emitError(new Error("tus: unable to create upload because no endpoint is provided"))}},{key:"_resumeUpload",value:function(){var e=this,t=(0,s.newRequest)();t.open("HEAD",this.url,!0),t.onload=function(){if(!p(t.status,200))return e._hasStorage()&&p(t.status,400)&&e._storage.removeItem(e._fingerprint,(function(t){t&&e._emitError(t)})),423===t.status?void e._emitXhrError(t,new Error("tus: upload is currently locked; retry later")):e.options.endpoint?(e.url=null,void e._createUpload()):void e._emitXhrError(t,new Error("tus: unable to resume upload (new upload cannot be created without an endpoint)"));var r=parseInt(t.getResponseHeader("Upload-Offset"),10);if(isNaN(r))e._emitXhrError(t,new Error("tus: invalid or missing offset value"));else{var n=parseInt(t.getResponseHeader("Upload-Length"),10);if(!isNaN(n)||e.options.uploadLengthDeferred){if(r===n)return e._emitProgress(n,n),void e._emitSuccess();e._offset=r,e._startUpload()}else e._emitXhrError(t,new Error("tus: invalid or missing length value"))}},t.onerror=function(r){e._emitXhrError(t,new Error("tus: failed to resume upload"),r)},this._setupXHR(t),t.send(null)}},{key:"_startUpload",value:function(){var e=this;if(!this._aborted){var t=(0,s.newRequest)();this.options.overridePatchMethod?(t.open("POST",this.url,!0),t.setRequestHeader("X-HTTP-Method-Override","PATCH")):t.open("PATCH",this.url,!0),t.onload=function(){p(t.status,200)?e._handleUploadResponse(t):e._emitXhrError(t,new Error("tus: unexpected response while uploading chunk"))},t.onerror=function(r){e._aborted||e._emitXhrError(t,new Error("tus: failed to upload chunk at offset "+e._offset),r)},this._setupXHR(t),t.setRequestHeader("Upload-Offset",this._offset),this._addChunkToRequest(t)}}},{key:"_addChunkToRequest",value:function(e){var t=this;"upload"in e&&(e.upload.onprogress=function(e){e.lengthComputable&&t._emitProgress(r+e.loaded,t._size)}),e.setRequestHeader("Content-Type","application/offset+octet-stream");var r=this._offset,n=this._offset+this.options.chunkSize;(n===1/0||n>this._size)&&!this.options.uploadLengthDeferred&&(n=this._size),this._source.slice(r,n,(function(r,n,o){r?t._emitError(r):(t.options.uploadLengthDeferred&&o&&(t._size=t._offset+(n&&n.size?n.size:0),e.setRequestHeader("Upload-Length",t._size)),null===n?e.send():(e.send(n),t._emitProgress(t._offset,t._size)))}))}},{key:"_handleUploadResponse",value:function(e){var t=this,r=parseInt(e.getResponseHeader("Upload-Offset"),10);if(isNaN(r))this._emitXhrError(e,new Error("tus: invalid or missing offset value"));else{if(this._emitProgress(r,this._size),this._emitChunkComplete(r-this._offset,r,this._size),this._offset=r,r==this._size)return this.options.removeFingerprintOnSuccess&&this.options.resume&&this._storage.removeItem(this._fingerprint,(function(e){e&&t._emitError(e)})),this._emitSuccess(),void this._source.close();this._startUpload()}}}],[{key:"terminate",value:function(e,t,r){if("function"!=typeof t&&"function"!=typeof r)throw new Error("tus: a callback function must be specified");"function"==typeof t&&(r=t,t={});var n=(0,s.newRequest)();n.open("DELETE",e,!0),n.onload=function(){204===n.status?r():r(new o.default(new Error("tus: unexpected response while terminating upload"),null,n))},n.onerror=function(e){r(new o.default(e,new Error("tus: failed to terminate upload"),n))},h(n,t),n.send(null)}}]),e}();function p(e,t){return e>=t&&e<t+100}function h(e,t){e.setRequestHeader("Tus-Resumable","1.0.0");var r=t.headers||{};for(var n in r)e.setRequestHeader(n,r[n]);e.withCredentials=t.withCredentials}d.defaultOptions=c,t.default=d},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=function(e){function t(e){var r=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t);var o=function(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!=typeof t&&"function"!=typeof t?e:t}(this,(t.__proto__||Object.getPrototypeOf(t)).call(this,e.message));o.originalRequest=n,o.causingError=r;var i=e.message;return null!=r&&(i+=", caused by "+r.toString()),null!=n&&(i+=", originated from request (response code: "+n.status+", response text: "+n.responseText+")"),o.message=i,o}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}(t,Error),t}();t.default=n},function(e,t,r){"use strict";var n=Object.prototype.hasOwnProperty,o=Object.prototype.toString,i=Object.defineProperty,a=Object.getOwnPropertyDescriptor,s=function(e){return"function"==typeof Array.isArray?Array.isArray(e):"[object Array]"===o.call(e)},u=function(e){if(!e||"[object Object]"!==o.call(e))return!1;var t,r=n.call(e,"constructor"),i=e.constructor&&e.constructor.prototype&&n.call(e.constructor.prototype,"isPrototypeOf");if(e.constructor&&!r&&!i)return!1;for(t in e);return void 0===t||n.call(e,t)},l=function(e,t){i&&"__proto__"===t.name?i(e,t.name,{enumerable:!0,configurable:!0,value:t.newValue,writable:!0}):e[t.name]=t.newValue},f=function(e,t){if("__proto__"===t){if(!n.call(e,t))return;if(a)return a(e,t).value}return e[t]};e.exports=function e(){var t,r,n,o,i,a,c=arguments[0],d=1,p=arguments.length,h=!1;for("boolean"==typeof c&&(h=c,c=arguments[1]||{},d=2),(null==c||"object"!=typeof c&&"function"!=typeof c)&&(c={});d<p;++d)if(null!=(t=arguments[d]))for(r in t)n=f(c,r),c!==(o=f(t,r))&&(h&&o&&(u(o)||(i=s(o)))?(i?(i=!1,a=n&&s(n)?n:[]):a=n&&u(n)?n:{},l(c,{name:r,newValue:e(h,a,o)})):void 0!==o&&l(c,{name:r,newValue:o}));return c}},function(module,exports,__webpack_require__){(function(global){var __WEBPACK_AMD_DEFINE_ARRAY__,__WEBPACK_AMD_DEFINE_RESULT__;!function(e,t){module.exports=t(e)}("undefined"!=typeof self?self:"undefined"!=typeof window?window:void 0!==global?global:this,(function(global){"use strict";global=global||{};var _Base64=global.Base64,version="2.5.1",buffer;if(module.exports)try{buffer=eval("require('buffer').Buffer")}catch(e){buffer=void 0}var b64chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",b64tab=function(e){for(var t={},r=0,n=e.length;r<n;r++)t[e.charAt(r)]=r;return t}(b64chars),fromCharCode=String.fromCharCode,cb_utob=function(e){if(e.length<2)return(t=e.charCodeAt(0))<128?e:t<2048?fromCharCode(192|t>>>6)+fromCharCode(128|63&t):fromCharCode(224|t>>>12&15)+fromCharCode(128|t>>>6&63)+fromCharCode(128|63&t);var t=65536+1024*(e.charCodeAt(0)-55296)+(e.charCodeAt(1)-56320);return fromCharCode(240|t>>>18&7)+fromCharCode(128|t>>>12&63)+fromCharCode(128|t>>>6&63)+fromCharCode(128|63&t)},re_utob=/[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g,utob=function(e){return e.replace(re_utob,cb_utob)},cb_encode=function(e){var t=[0,2,1][e.length%3],r=e.charCodeAt(0)<<16|(e.length>1?e.charCodeAt(1):0)<<8|(e.length>2?e.charCodeAt(2):0);return[b64chars.charAt(r>>>18),b64chars.charAt(r>>>12&63),t>=2?"=":b64chars.charAt(r>>>6&63),t>=1?"=":b64chars.charAt(63&r)].join("")},btoa=global.btoa?function(e){return global.btoa(e)}:function(e){return e.replace(/[\s\S]{1,3}/g,cb_encode)},_encode=buffer?buffer.from&&Uint8Array&&buffer.from!==Uint8Array.from?function(e){return(e.constructor===buffer.constructor?e:buffer.from(e)).toString("base64")}:function(e){return(e.constructor===buffer.constructor?e:new buffer(e)).toString("base64")}:function(e){return btoa(utob(e))},encode=function(e,t){return t?_encode(String(e)).replace(/[+\/]/g,(function(e){return"+"==e?"-":"_"})).replace(/=/g,""):_encode(String(e))},encodeURI=function(e){return encode(e,!0)},re_btou=new RegExp(["[À-ß][-¿]","[à-ï][-¿]{2}","[ð-÷][-¿]{3}"].join("|"),"g"),cb_btou=function(e){switch(e.length){case 4:var t=((7&e.charCodeAt(0))<<18|(63&e.charCodeAt(1))<<12|(63&e.charCodeAt(2))<<6|63&e.charCodeAt(3))-65536;return fromCharCode(55296+(t>>>10))+fromCharCode(56320+(1023&t));case 3:return fromCharCode((15&e.charCodeAt(0))<<12|(63&e.charCodeAt(1))<<6|63&e.charCodeAt(2));default:return fromCharCode((31&e.charCodeAt(0))<<6|63&e.charCodeAt(1))}},btou=function(e){return e.replace(re_btou,cb_btou)},cb_decode=function(e){var t=e.length,r=t%4,n=(t>0?b64tab[e.charAt(0)]<<18:0)|(t>1?b64tab[e.charAt(1)]<<12:0)|(t>2?b64tab[e.charAt(2)]<<6:0)|(t>3?b64tab[e.charAt(3)]:0),o=[fromCharCode(n>>>16),fromCharCode(n>>>8&255),fromCharCode(255&n)];return o.length-=[0,0,2,1][r],o.join("")},_atob=global.atob?function(e){return global.atob(e)}:function(e){return e.replace(/\S{1,4}/g,cb_decode)},atob=function(e){return _atob(String(e).replace(/[^A-Za-z0-9\+\/]/g,""))},_decode=buffer?buffer.from&&Uint8Array&&buffer.from!==Uint8Array.from?function(e){return(e.constructor===buffer.constructor?e:buffer.from(e,"base64")).toString()}:function(e){return(e.constructor===buffer.constructor?e:new buffer(e,"base64")).toString()}:function(e){return btou(_atob(e))},decode=function(e){return _decode(String(e).replace(/[-_]/g,(function(e){return"-"==e?"+":"/"})).replace(/[^A-Za-z0-9\+\/]/g,""))},noConflict=function(){var e=global.Base64;return global.Base64=_Base64,e};if(global.Base64={VERSION:version,atob:atob,btoa:btoa,fromBase64:decode,toBase64:encode,utob:utob,encode:encode,encodeURI:encodeURI,btou:btou,decode:decode,noConflict:noConflict,__buffer__:buffer},"function"==typeof Object.defineProperty){var noEnum=function(e){return{value:e,enumerable:!1,writable:!0,configurable:!0}};global.Base64.extendString=function(){Object.defineProperty(String.prototype,"fromBase64",noEnum((function(){return decode(this)}))),Object.defineProperty(String.prototype,"toBase64",noEnum((function(e){return encode(this,e)}))),Object.defineProperty(String.prototype,"toBase64URI",noEnum((function(){return encode(this,!0)})))}}return global.Meteor&&(Base64=global.Base64),module.exports?module.exports.Base64=global.Base64:(__WEBPACK_AMD_DEFINE_ARRAY__=[],__WEBPACK_AMD_DEFINE_RESULT__=function(){return global.Base64}.apply(exports,__WEBPACK_AMD_DEFINE_ARRAY__),void 0===__WEBPACK_AMD_DEFINE_RESULT__||(module.exports=__WEBPACK_AMD_DEFINE_RESULT__)),{Base64:global.Base64}}))}).call(this,__webpack_require__(0))},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.newRequest=function(){return new window.XMLHttpRequest},t.resolveUrl=function(e,t){return new i.default(t,e).toString()};var n,o=r(12),i=(n=o)&&n.__esModule?n:{default:n}},function(e,t,r){"use strict";(function(t){var n=r(13),o=r(14),i=/^[A-Za-z][A-Za-z0-9+-.]*:\/\//,a=/^([a-z][a-z0-9.+-]*:)?(\/\/)?([\S\s]*)/i,s=new RegExp("^[\\x09\\x0A\\x0B\\x0C\\x0D\\x20\\xA0\\u1680\\u180E\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200A\\u202F\\u205F\\u3000\\u2028\\u2029\\uFEFF]+");function u(e){return(e||"").toString().replace(s,"")}var l=[["#","hash"],["?","query"],function(e){return e.replace("\\","/")},["/","pathname"],["@","auth",1],[NaN,"host",void 0,1,1],[/:(\d+)$/,"port",void 0,1],[NaN,"hostname",void 0,1,1]],f={hash:1,query:1};function c(e){var r,n=("undefined"!=typeof window?window:void 0!==t?t:"undefined"!=typeof self?self:{}).location||{},o={},a=typeof(e=e||n);if("blob:"===e.protocol)o=new p(unescape(e.pathname),{});else if("string"===a)for(r in o=new p(e,{}),f)delete o[r];else if("object"===a){for(r in e)r in f||(o[r]=e[r]);void 0===o.slashes&&(o.slashes=i.test(e.href))}return o}function d(e){e=u(e);var t=a.exec(e);return{protocol:t[1]?t[1].toLowerCase():"",slashes:!!t[2],rest:t[3]}}function p(e,t,r){if(e=u(e),!(this instanceof p))return new p(e,t,r);var i,a,s,f,h,_,v=l.slice(),m=typeof t,b=this,g=0;for("object"!==m&&"string"!==m&&(r=t,t=null),r&&"function"!=typeof r&&(r=o.parse),t=c(t),i=!(a=d(e||"")).protocol&&!a.slashes,b.slashes=a.slashes||i&&t.slashes,b.protocol=a.protocol||t.protocol||"",e=a.rest,a.slashes||(v[3]=[/(.*)/,"pathname"]);g<v.length;g++)"function"!=typeof(f=v[g])?(s=f[0],_=f[1],s!=s?b[_]=e:"string"==typeof s?~(h=e.indexOf(s))&&("number"==typeof f[2]?(b[_]=e.slice(0,h),e=e.slice(h+f[2])):(b[_]=e.slice(h),e=e.slice(0,h))):(h=s.exec(e))&&(b[_]=h[1],e=e.slice(0,h.index)),b[_]=b[_]||i&&f[3]&&t[_]||"",f[4]&&(b[_]=b[_].toLowerCase())):e=f(e);r&&(b.query=r(b.query)),i&&t.slashes&&"/"!==b.pathname.charAt(0)&&(""!==b.pathname||""!==t.pathname)&&(b.pathname=function(e,t){if(""===e)return t;for(var r=(t||"/").split("/").slice(0,-1).concat(e.split("/")),n=r.length,o=r[n-1],i=!1,a=0;n--;)"."===r[n]?r.splice(n,1):".."===r[n]?(r.splice(n,1),a++):a&&(0===n&&(i=!0),r.splice(n,1),a--);return i&&r.unshift(""),"."!==o&&".."!==o||r.push(""),r.join("/")}(b.pathname,t.pathname)),n(b.port,b.protocol)||(b.host=b.hostname,b.port=""),b.username=b.password="",b.auth&&(f=b.auth.split(":"),b.username=f[0]||"",b.password=f[1]||""),b.origin=b.protocol&&b.host&&"file:"!==b.protocol?b.protocol+"//"+b.host:"null",b.href=b.toString()}p.prototype={set:function(e,t,r){var i=this;switch(e){case"query":"string"==typeof t&&t.length&&(t=(r||o.parse)(t)),i[e]=t;break;case"port":i[e]=t,n(t,i.protocol)?t&&(i.host=i.hostname+":"+t):(i.host=i.hostname,i[e]="");break;case"hostname":i[e]=t,i.port&&(t+=":"+i.port),i.host=t;break;case"host":i[e]=t,/:\d+$/.test(t)?(t=t.split(":"),i.port=t.pop(),i.hostname=t.join(":")):(i.hostname=t,i.port="");break;case"protocol":i.protocol=t.toLowerCase(),i.slashes=!r;break;case"pathname":case"hash":if(t){var a="pathname"===e?"/":"#";i[e]=t.charAt(0)!==a?a+t:t}else i[e]=t;break;default:i[e]=t}for(var s=0;s<l.length;s++){var u=l[s];u[4]&&(i[u[1]]=i[u[1]].toLowerCase())}return i.origin=i.protocol&&i.host&&"file:"!==i.protocol?i.protocol+"//"+i.host:"null",i.href=i.toString(),i},toString:function(e){e&&"function"==typeof e||(e=o.stringify);var t,r=this,n=r.protocol;n&&":"!==n.charAt(n.length-1)&&(n+=":");var i=n+(r.slashes?"//":"");return r.username&&(i+=r.username,r.password&&(i+=":"+r.password),i+="@"),i+=r.host+r.pathname,(t="object"==typeof r.query?e(r.query):r.query)&&(i+="?"!==t.charAt(0)?"?"+t:t),r.hash&&(i+=r.hash),i}},p.extractProtocol=d,p.location=c,p.trimLeft=u,p.qs=o,e.exports=p}).call(this,r(0))},function(e,t,r){"use strict";e.exports=function(e,t){if(t=t.split(":")[0],!(e=+e))return!1;switch(t){case"http":case"ws":return 80!==e;case"https":case"wss":return 443!==e;case"ftp":return 21!==e;case"gopher":return 70!==e;case"file":return!1}return 0!==e}},function(e,t,r){"use strict";var n,o=Object.prototype.hasOwnProperty;function i(e){try{return decodeURIComponent(e.replace(/\+/g," "))}catch(e){return null}}t.stringify=function(e,t){t=t||"";var r,i,a=[];for(i in"string"!=typeof t&&(t="?"),e)if(o.call(e,i)){if((r=e[i])||null!==r&&r!==n&&!isNaN(r)||(r=""),i=encodeURIComponent(i),r=encodeURIComponent(r),null===i||null===r)continue;a.push(i+"="+r)}return a.length?t+a.join("&"):""},t.parse=function(e){for(var t,r=/([^=?&]+)=?([^&]*)/g,n={};t=r.exec(e);){var o=i(t[1]),a=i(t[2]);null===o||null===a||o in n||(n[o]=a)}return n}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=function(){function e(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}return function(t,r,n){return r&&e(t.prototype,r),n&&e(t,n),t}}();t.getSource=function(e,t,r){if((0,o.default)()&&e&&void 0!==e.uri)return void(0,i.default)(e.uri,(function(e,t){if(e)return r(new Error("tus: cannot fetch `file.uri` as Blob, make sure the uri is correct and accessible. "+e));r(null,new f(t))}));if("function"==typeof e.slice&&void 0!==e.size)return void r(null,new f(e));if("function"==typeof e.read)return t=+t,isFinite(t)?void r(null,new c(e,t)):void r(new Error("cannot create source for stream without a finite value for the `chunkSize` option"));r(new Error("source object may only be an instance of File, Blob, or Reader in this environment"))};var o=u(r(1)),i=u(r(16)),a=u(r(17)),s=u(r(18));function u(e){return e&&e.__esModule?e:{default:e}}function l(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}var f=function(){function e(t){l(this,e),this._file=t,this.size=t.size}return n(e,[{key:"slice",value:function(e,t,r){(0,a.default)()?(0,s.default)(this._file.slice(e,t),(function(e,t){if(e)return r(e);r(null,t)})):r(null,this._file.slice(e,t))}},{key:"close",value:function(){}}]),e}(),c=function(){function e(t,r){l(this,e),this._chunkSize=r,this._buffer=void 0,this._bufferOffset=0,this._reader=t,this._done=!1}return n(e,[{key:"slice",value:function(e,t,r){if(!(e<this._bufferOffset))return this._readUntilEnoughDataOrDone(e,t,r);r(new Error("Requested data is before the reader's current offset"))}},{key:"_readUntilEnoughDataOrDone",value:function(e,t,r){var n=this,o=t<=this._bufferOffset+d(this._buffer);if(this._done||o){var i=this._getDataFromBuffer(e,t);r(null,i,null==i&&this._done)}else this._reader.read().then((function(o){var i=o.value;o.done?n._done=!0:void 0===n._buffer?n._buffer=i:n._buffer=function(e,t){if(e.concat)return e.concat(t);if(e instanceof Blob)return new Blob([e,t],{type:e.type});if(e.set){var r=new e.constructor(e.length+t.length);return r.set(e),r.set(t,e.length),r}throw new Error("Unknown data type")}(n._buffer,i),n._readUntilEnoughDataOrDone(e,t,r)})).catch((function(e){r(new Error("Error during read: "+e))}))}},{key:"_getDataFromBuffer",value:function(e,t){e>this._bufferOffset&&(this._buffer=this._buffer.slice(e-this._bufferOffset),this._bufferOffset=e);var r=0===d(this._buffer);return this._done&&r?null:this._buffer.slice(0,t-e)}},{key:"close",value:function(){this._reader.cancel&&this._reader.cancel()}}]),e}();function d(e){return void 0===e?0:void 0!==e.size?e.size:e.length}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t){var r=new XMLHttpRequest;r.responseType="blob",r.onload=function(){var e=r.response;t(null,e)},r.onerror=function(e){t(e)},r.open("GET",e),r.send()}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0});t.default=function(){return"undefined"!=typeof window&&(void 0!==window.PhoneGap||void 0!==window.Cordova||void 0!==window.cordova)}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t){var r=new FileReader;r.onload=function(){t(null,new Uint8Array(r.result))},r.onerror=function(e){t(e)},r.readAsArrayBuffer(e)}},function(e,t,r){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t,r){if((0,i.default)())return r(null,function(e,t){var r=e.exif?function(e){var t=0;if(0===e.length)return t;for(var r=0;r<e.length;r++){var n=e.charCodeAt(r);t=(t<<5)-t+n,t&=t}return t}(JSON.stringify(e.exif)):"noexif";return["tus-rn",e.name||"noname",e.size||"nosize",r,t.endpoint].join("/")}(e,t));return r(null,["tus-br",e.name,e.type,e.size,e.lastModified,t.endpoint].join("-"))};var n,o=r(1),i=(n=o)&&n.__esModule?n:{default:n}}]);
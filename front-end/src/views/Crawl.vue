<template>
<div>
  <div class="s009">
      <form>
        <div class="inner-form">
          <a-tabs :default-active-key="1" @change="onChangeTab" class="form-crawl">
          <a-tab-pane
            :key="1"
            tab="Crawl Specific Link"
          >
            <div  class="basic-search">
                  
                    <div style="margin-right: 20px">
                    <a-input  size="large" id="linkcrawl" v-model="linkcrawl" name="linkcrawl" type="text" placeholder="Enter link for crawl" />
                    </div>
                  
                  <div class="advance-search">
                  <div class="row third">
                    <div class="input-field">
                      <div class="result-count">
                      </div>
                      <div class="group-btn">
                        <a-button class="btn-delete" @click="linkcrawl===null">RESET</a-button>
                        <a-button
                          type="primary"
                          class="btn-crawl"
                          @click="show=true"
                          >CRAWL</a-button
                        >
                      </div>
                    </div>
                  </div>   
                  </div>     
                </div>
          </a-tab-pane>
          <a-tab-pane
            :key="2"
            tab="Crawl Category"
            force-render
          >
            <div class="advance-search">
                  <span class="desc">ADVANCED CRAWL</span>
                  <div style="display: flex; flex-wrap : wrap">
                    <treeselect class="crawl-choice-field"
                        :multiple="false"
                        :show-count="true"
                        :options="CategoryByDomain"
                        v-model="valueCategory"
                        placeholder="Choose Category"
                        v-on:input="ChooseRangeScore"
                        v-on:select="ChooseRangeScore"
                        v-on:deselect="ChooseRangeScore"
                        v-on:close="ChooseRangeScore"
                      />
                    <treeselect class="crawl-choice-field"
                        :multiple="false"
                        :show-count="true"
                        :options="Depth"
                        v-model="valueDepth"
                        placeholder="Choose Depth"
                        v-on:input="ChooseRangeScore"
                        v-on:select="ChooseRangeScore"
                        v-on:deselect="ChooseRangeScore"
                        v-on:close="ChooseRangeScore"
                      />
                  </div>
                  <div class="row third">
                  <div class="input-field">
                    <div class="result-count">
                    </div>
                    <div class="group-btn">
                      <a-button class="btn-delete" @click="valueCategory=null, valueDepth=null">RESET</a-button>
                        <a-button
                          type="primary"
                          class="btn-crawl"
                          @click="show=true"
                          >CRAWL</a-button
                        >
                    </div>
                  </div>
                </div>
                </div>
          </a-tab-pane>
          <a-tab-pane
            :key="3"
            tab="Crawl Domain"
            force-render
          >
            <div class="advance-search">
                  <span class="desc">ADVANCED CRAWL</span>
                  <div style="display: flex; flex-wrap : wrap">
                    <treeselect class="crawl-choice-field"
                        :multiple="false"
                        :show-count="true"
                        :options="Domain"
                        v-model="valueDomain"
                        placeholder="Choose Domain"
                      />
                  </div>
                  <div class="row third">
                    <div class="input-field">
                      <div class="result-count">
                      </div>
                      <div class="group-btn">
                        <a-button class="btn-delete" @click="valueCategory=null">RESET</a-button>
                        <a-button
                          type="primary"
                          class="btn-crawl"
                          @click="show=true"
                          >CRAWL</a-button
                        >
                      </div>
                    </div>
                  </div>
                </div>
          </a-tab-pane>
        </a-tabs>
        </div>
      </form>
    </div>

    <a-modal v-model="show" title="Confirm" style="margin-top: 180px;" >
    <template v-slot:footer>
        <a-button class="btn-redirect" key="back" @click="show=false, showLoading=true, onClickCrawl()">
          Redirect me to page
        </a-button>
        <a-button class="btn-import" key="submit" type="primary" :loading="loading" @click="show=false, showLoading=true, onClickCrawlImport()">
          Auto import
        </a-button>
    </template>
      <p style="font-size: medium;">
      Do you want to delivered to another page after process Named Entity Recognization
      or auto import to Neo4j database after process Named Entity Recognization without route?
      </p>
      <p style="font-size: medium;">
      Please select score that entity be import to database
      </p>
      <treeselect style="width: 130px; margin-left: 5px; align-self: center;"
        :multiple="false"
        :options="RangeScore"
        v-model="valueRangeScore"
        placeholder="All Score"
        v-on:input="filterColumn"
        v-on:select="filterColumn"
        v-on:deselect="filterColumn"
        v-on:close="filterColumn"
      />
    </a-modal>

    <a-modal v-model="showLoading" style="margin-top: 180px;"
     :ok-button-props="{ style: { display: 'none' } }"
      :cancel-button-props="{ style: { display: 'none' } }" :maskClosable="false" :closable="false">
      <br>
      <preloader />
      <br>
      <p style="text-align: center;">Crawl in progress. It will take some minutes. Please wait...</p>
    </a-modal>
</div>
</template>

<script>
import axios from "axios"
import jwt_decode from "jwt-decode"
import Treeselect from 'vue3-treeselect'
import Preloader from '../components/PreLoader.vue'
import 'vue3-treeselect/dist/vue3-treeselect.css'
import DomainCategory from '../data/data.json';
export default {
  name: "CrawlComponent",
  props: {
  },
  components: { Treeselect, Preloader},
  data() {
    return {
      show: false,
      showLoading: false,
      modalClass: '',
      RangeScore: [
      { id: 0.9, label: '>= 90%' },
      { id: 0.8, label: '>= 80%' },
      { id: 0.75, label: '>= 75%' },
      { id: 0.7, label: '>= 70%' }
      ],
      type: 1,
      selected: ['coursera'],
      options: [
      { value: null, text: 'Please select one domain', disabled: true  },
      { value: 'coursera', text: 'Coursera' },
      { value: 'udemy', text: 'Udemy' },
      { value: 'edx', text: 'Edx' },
      { value: 'ed2go', text: 'Ed2go'},
      { value: 'udacity', text: 'Udacity'},
      { value: 'Linkin', text: 'Linkin Learning'},
      ],
      Domain: [
        {id: 'coursera', label: 'Coursera'},
        {id: 'udemy', label: 'Udemy'},
        {id: 'edx', label: 'Edx'},
        {id: 'ed2go', label: 'Ed2go'},
        {id: 'udacity', label: 'Udacity'},
      ],
      CategoryByDomain: DomainCategory,
        value: null,
      Depth: [
        {id: 'all', label: 'All'},
        {id: 5, label: 5},
        {id: 10, label: 10},
        {id: 20, label: 20},
        {id: 50, label: 50}
      ],
    }
  },
  created(){
    if(!localStorage.getItem("token") || !jwt_decode(localStorage.getItem("token")).is_dataadmin) {
      this.$router.push({
        path: `/`,
      });
    }
  },
  methods: {
    onChangeTab(key) {
      this.type = key
    },
    async onClickCrawl() {
      console.log("AAA:", this.type)
      console.log(this.valueCategory)
      await axios
        .post(`api/crawl_train/`, {
          type: this.type,
          linkcrawl: this.linkcrawl,
          category: this.valueCategory,
          domain: this.valueDomain,
          depth: this.valueDepth
          }
        )
        .then(result => {
          console.log("True")
          this.$router.push({
            name: 'NER',
            params: {train_output: (JSON.parse(result.data))['train_output']},
          });
        })
        .catch((err) => {
          console.log(err);
          this.showLoading = false;
          alert("Crawl process fail!")
        });
    },
    async onClickCrawlImport() {
      await axios
        .post(`api/crawl_train_import/`, {
         type: this.type,
          linkcrawl: this.linkcrawl,
          category: this.valueCategory,
          domain: this.valueDomain,
          depth: this.valueDepth,
          score: this.valueRangeScore
          }
        )
        .then(() => {
          console.log("True")
          this.showLoading = false;
          alert("Crawl process success!")
          this.$router.push({
            path: '/dashboard',
          });
        })
        .catch((err) => {
          console.log(err);
          this.showLoading = false;
          alert("Crawl process fail!")
        });
    },
  }
};
</script>
<style src="vue3-treeselect/dist/vue3-treeselect.css">
</style>
<style lang="scss">
.s009 form {
}
.form-crawl, .inner-form {
  display: block !important;
}
.ant-message-custom-content i{
  top: -3px !important;
}
.form-crawl .ant-tabs-tab-active,
.form-crawl .ant-tabs-tab:hover {
  color: rgb(68, 211, 68) !important;
  // margin-left: 3.5rem !important;
}

.form-crawl .ant-tabs-ink-bar {
  color: rgb(68, 211, 68) !important;
  background-color: rgb(68, 211, 68) !important;
}
.form-crawl .ant-tabs-bar {
  background-color: white !important;
  margin-bottom: 0px !important;
}
.sub-menu{
  position: absolute;            
    min-width: 10rem;
    padding: .5rem 0;
    margin: .125rem 0 0;
    font-size: 1rem;
    color: #212529;
    text-align: left;
    list-style: none;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid rgba(0,0,0,.15);
    border-radius: .25rem;
}
html {
  line-height: 1.15;
  /* 1 */
  -ms-text-size-adjust: 100%;
  /* 2 */
  -webkit-text-size-adjust: 100%;
  /* 2 */
}

/* Sections
   ========================================================================== */
/**
 * Remove the margin in all browsers (opinionated).
 */
body {
  margin: 0;
}

/**
 * Add the correct display in IE 9-.
 */
article,
aside,
footer,
header,
nav,
section {
  display: block;
}

/**
 * Correct the font size and margin on `h1` elements within `section` and
 * `article` contexts in Chrome, Firefox, and Safari.
 */
h1 {
  font-size: 2em;
  margin: 0.67em 0;
}

/* Grouping content
   ========================================================================== */
/**
 * Add the correct display in IE 9-.
 * 1. Add the correct display in IE.
 */
figcaption,
figure,
main {
  /* 1 */
  display: block;
}

/**
 * Add the correct margin in IE 8.
 */
figure {
  margin: 1em 40px;
}

/**
 * 1. Add the correct box sizing in Firefox.
 * 2. Show the overflow in Edge and IE.
 */
hr {
  box-sizing: content-box;
  /* 1 */
  height: 0;
  /* 1 */
  overflow: visible;
  /* 2 */
}

/**
 * 1. Correct the inheritance and scaling of font size in all browsers.
 * 2. Correct the odd `em` font sizing in all browsers.
 */
pre {
  font-family: monospace, monospace;
  /* 1 */
  font-size: 1em;
  /* 2 */
}

/* Text-level semantics
   ========================================================================== */
/**
 * 1. Remove the gray background on active links in IE 10.
 * 2. Remove gaps in links underline in iOS 8+ and Safari 8+.
 */
a {
  background-color: transparent;
  /* 1 */
  -webkit-text-decoration-skip: objects;
  /* 2 */
}

/**
 * 1. Remove the bottom border in Chrome 57- and Firefox 39-.
 * 2. Add the correct text decoration in Chrome, Edge, IE, Opera, and Safari.
 */
abbr[title] {
  border-bottom: none;
  /* 1 */
  text-decoration: underline;
  /* 2 */
  text-decoration: underline dotted;
  /* 2 */
}

/**
 * Prevent the duplicate application of `bolder` by the next rule in Safari 6.
 */
b,
strong {
  font-weight: inherit;
}

/**
 * Add the correct font weight in Chrome, Edge, and Safari.
 */
b,
strong {
  font-weight: bolder;
}

/**
 * 1. Correct the inheritance and scaling of font size in all browsers.
 * 2. Correct the odd `em` font sizing in all browsers.
 */
code,
kbd,
samp {
  font-family: monospace, monospace;
  /* 1 */
  font-size: 1em;
  /* 2 */
}

/**
 * Add the correct font style in Android 4.3-.
 */
dfn {
  font-style: italic;
}

/**
 * Add the correct background and color in IE 9-.
 */
mark {
  background-color: #ff0;
  color: #000;
}

/**
 * Add the correct font size in all browsers.
 */
small {
  font-size: 80%;
}

/**
 * Prevent `sub` and `sup` elements from affecting the line height in
 * all browsers.
 */
sub,
sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}

sub {
  bottom: -0.25em;
}

sup {
  top: -0.5em;
}

/* Embedded content
   ========================================================================== */
/**
 * Add the correct display in IE 9-.
 */
audio,
video {
  display: inline-block;
}

/**
 * Add the correct display in iOS 4-7.
 */
audio:not([controls]) {
  display: none;
  height: 0;
}

/**
 * Remove the border on images inside links in IE 10-.
 */
img {
  border-style: none;
}

/**
 * Hide the overflow in IE.
 */
svg:not(:root) {
  overflow: hidden;
}

/* Forms
   ========================================================================== */
/**
 * 1. Change the font styles in all browsers (opinionated).
 * 2. Remove the margin in Firefox and Safari.
 */
button,
input,
optgroup,
select,
textarea {
  font-family: sans-serif;
  /* 1 */
  font-size: 100%;
  /* 1 */
  line-height: 1.15;
  /* 1 */
  margin: 0;
  /* 2 */
}

/**
 * Show the overflow in IE.
 * 1. Show the overflow in Edge.
 */
button,
input {
  /* 1 */
  overflow: visible;
}

/**
 * Remove the inheritance of text transform in Edge, Firefox, and IE.
 * 1. Remove the inheritance of text transform in Firefox.
 */
button,
select {
  /* 1 */
  text-transform: none;
}

/**
 * 1. Prevent a WebKit bug where (2) destroys native `audio` and `video`
 *    controls in Android 4.
 * 2. Correct the inability to style clickable types in iOS and Safari.
 */
button,
html [type="button"],
[type="reset"],
[type="submit"] {
  -webkit-appearance: button;
  /* 2 */
}

/**
 * Remove the inner border and padding in Firefox.
 */
button::-moz-focus-inner,
[type="button"]::-moz-focus-inner,
[type="reset"]::-moz-focus-inner,
[type="submit"]::-moz-focus-inner {
  border-style: none;
  padding: 0;
}

/**
 * Restore the focus styles unset by the previous rule.
 */
button:-moz-focusring,
[type="button"]:-moz-focusring,
[type="reset"]:-moz-focusring,
[type="submit"]:-moz-focusring {
  outline: 1px dotted ButtonText;
}

/**
 * Correct the padding in Firefox.
 */
fieldset {
  padding: 0.35em 0.75em 0.625em;
}

/**
 * 1. Correct the text wrapping in Edge and IE.
 * 2. Correct the color inheritance from `fieldset` elements in IE.
 * 3. Remove the padding so developers are not caught out when they zero out
 *    `fieldset` elements in all browsers.
 */
legend {
  box-sizing: border-box;
  /* 1 */
  color: inherit;
  /* 2 */
  display: table;
  /* 1 */
  max-width: 100%;
  /* 1 */
  padding: 0;
  /* 3 */
  white-space: normal;
  /* 1 */
}

/**
 * 1. Add the correct display in IE 9-.
 * 2. Add the correct vertical alignment in Chrome, Firefox, and Opera.
 */
progress {
  display: inline-block;
  /* 1 */
  vertical-align: baseline;
  /* 2 */
}

/**
 * Remove the default vertical scrollbar in IE.
 */
textarea {
  overflow: auto;
}

/**
 * 1. Add the correct box sizing in IE 10-.
 * 2. Remove the padding in IE 10-.
 */
[type="checkbox"],
[type="radio"] {
  box-sizing: border-box;
  /* 1 */
  padding: 0;
  /* 2 */
}

/**
 * Correct the cursor style of increment and decrement buttons in Chrome.
 */
[type="number"]::-webkit-inner-spin-button,
[type="number"]::-webkit-outer-spin-button {
  height: auto;
}

/**
 * 1. Correct the odd appearance in Chrome and Safari.
 * 2. Correct the outline style in Safari.
 */
[type="search"] {
  -webkit-appearance: textfield;
  /* 1 */
  outline-offset: -2px;
  /* 2 */
}

/**
 * Remove the inner padding and cancel buttons in Chrome and Safari on macOS.
 */
[type="search"]::-webkit-search-cancel-button,
[type="search"]::-webkit-search-decoration {
  -webkit-appearance: none;
}

/**
 * 1. Correct the inability to style clickable types in iOS and Safari.
 * 2. Change font properties to `inherit` in Safari.
 */
::-webkit-file-upload-button {
  -webkit-appearance: button;
  /* 1 */
  font: inherit;
  /* 2 */
}

/* Interactive
   ========================================================================== */
/*
 * Add the correct display in IE 9-.
 * 1. Add the correct display in Edge, IE, and Firefox.
 */
details,
menu {
  display: block;
}

/*
 * Add the correct display in all browsers.
 */
summary {
  display: list-item;
}

/* Scripting
   ========================================================================== */
/**
 * Add the correct display in IE 9-.
 */
canvas {
  display: inline-block;
}

/**
 * Add the correct display in IE.
 */
template {
  display: none;
}

/* Hidden
   ========================================================================== */
/**
 * Add the correct display in IE 10-.
 */
[hidden] {
  display: none;
}

html {
  height: 100%;
}

fieldset {
  margin: 0;
  padding: 0;
  -webkit-margin-start: 0;
  -webkit-margin-end: 0;
  -webkit-padding-before: 0;
  -webkit-padding-start: 0;
  -webkit-padding-end: 0;
  -webkit-padding-after: 0;
  border: 0;
}

legend {
  margin: 0;
  padding: 0;
  display: block;
  -webkit-padding-start: 0;
  -webkit-padding-end: 0;
}

/*===============================
=            Choices            =
===============================*/
.choices {
  position: relative;
  margin-bottom: 24px;
  font-size: 16px;
}

.choices:focus {
  outline: none;
}

.choices:last-child {
  margin-bottom: 0;
}

.choices.is-disabled .choices__inner, .choices.is-disabled .choices__input {
  background-color: #EAEAEA;
  cursor: not-allowed;
  -webkit-user-select: none;
     -moz-user-select: none;
      -ms-user-select: none;
          user-select: none;
}

.choices.is-disabled .choices__item {
  cursor: not-allowed;
}

.choices[data-type*="select-one"] {
  cursor: pointer;
}

.choices[data-type*="select-one"] .choices__inner {
  padding-bottom: 7.5px;
}

.choices[data-type*="select-one"] .choices__input {
  display: block;
  width: 100%;
  padding: 10px;
  border-bottom: 1px solid #DDDDDD;
  background-color: #FFFFFF;
  margin: 0;
}

.choices[data-type*="select-one"] .choices__button {
  padding: 0;
  background-size: 8px;
  height: 100%;
  position: absolute;
  top: 50%;
  right: 0;
  margin-top: -10px;
  margin-right: 25px;
  height: 20px;
  width: 20px;
  border-radius: 10em;
  opacity: .5;
}

.choices[data-type*="select-one"] .choices__button:hover, .choices[data-type*="select-one"] .choices__button:focus {
  opacity: 1;
}

.choices[data-type*="select-one"] .choices__button:focus {
  box-shadow: 0px 0px 0px 2px #00BCD4;
}

.choices[data-type*="select-one"]:after {
  content: "";
  height: 0;
  width: 0;
  border-style: solid;
  border-color: #333333 transparent transparent transparent;
  border-width: 5px;
  position: absolute;
  right: 11.5px;
  top: 50%;
  margin-top: -2.5px;
  pointer-events: none;
}

.choices[data-type*="select-one"].is-open:after {
  border-color: transparent transparent #333333 transparent;
  margin-top: -7.5px;
}

.choices[data-type*="select-one"][dir="rtl"]:after {
  left: 11.5px;
  right: auto;
}

.choices[data-type*="select-one"][dir="rtl"] .choices__button {
  right: auto;
  left: 0;
  margin-left: 25px;
  margin-right: 0;
}

.choices[data-type*="select-multiple"] .choices__inner, .choices[data-type*="text"] .choices__inner {
  cursor: text;
}

.choices[data-type*="select-multiple"] .choices__button, .choices[data-type*="text"] .choices__button {
  position: relative;
  display: inline-block;
  margin-top: 0;
  margin-right: -4px;
  margin-bottom: 0;
  margin-left: 8px;
  padding-left: 16px;
  border-left: 1px solid #008fa1;
  background-size: 8px;
  width: 8px;
  line-height: 1;
  opacity: .75;
}

.choices[data-type*="select-multiple"] .choices__button:hover, .choices[data-type*="select-multiple"] .choices__button:focus, .choices[data-type*="text"] .choices__button:hover, .choices[data-type*="text"] .choices__button:focus {
  opacity: 1;
}

.choices__inner {
  display: inline-block;
  vertical-align: top;
  width: 100%;
  background-color: #f9f9f9;
  padding: 7.5px 7.5px 3.75px;
  border: 1px solid #DDDDDD;
  border-radius: 2.5px;
  font-size: 14px;
  min-height: 44px;
  overflow: hidden;
}

.is-focused .choices__inner, .is-open .choices__inner {
  border-color: #b7b7b7;
}

.is-open .choices__inner {
  border-radius: 2.5px 2.5px 0 0;
}

.is-flipped.is-open .choices__inner {
  border-radius: 0 0 2.5px 2.5px;
}

.choices__list {
  margin: 0;
  padding-left: 0;
  list-style: none;
}

.choices__list--single {
  display: inline-block;
  padding: 4px 16px 4px 4px;
  width: 100%;
}

[dir="rtl"] .choices__list--single {
  padding-right: 4px;
  padding-left: 16px;
}

.choices__list--single .choices__item {
  width: 100%;
}

.choices__list--multiple {
  display: inline;
}
.inner-form .ant-tabs-tabpane {
  margin-bottom: 150px !important; 
}

.choices__list--multiple .choices__item {
  display: inline-block;
  vertical-align: middle;
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  margin-right: 3.75px;
  margin-bottom: 3.75px;
  background-color: rgb(4, 250, 4);
  border: 1px solid rgb(4, 250, 4);
  color: #FFFFFF;
  word-break: break-all;
}

.choices__list--multiple .choices__item[data-deletable] {
  padding-right: 5px;
}

[dir="rtl"] .choices__list--multiple .choices__item {
  margin-right: 0;
  margin-left: 3.75px;
}

.choices__list--multiple .choices__item.is-highlighted {
  background-color: rgb(4, 250, 4);
  border: 1px solid rgb(4, 250, 4);
}

.is-disabled .choices__list--multiple .choices__item {
  background-color: #aaaaaa;
  border: 1px solid #919191;
}
.vue-treeselect__menu {
  max-height: 200px !important;
}
.choices__list--dropdown {
  display: none;
  z-index: 1;
  position: absolute;
  width: 100%;
  background-color: #FFFFFF;
  border: 1px solid #DDDDDD;
  top: 100%;
  margin-top: -1px;
  border-bottom-left-radius: 2.5px;
  border-bottom-right-radius: 2.5px;
  overflow: hidden;
  word-break: break-all;
}

.choices__list--dropdown.is-active {
  display: block;
}

.is-open .choices__list--dropdown {
  border-color: #b7b7b7;
}

.is-flipped .choices__list--dropdown {
  top: auto;
  bottom: 100%;
  margin-top: 0;
  margin-bottom: -1px;
  border-radius: .25rem .25rem 0 0;
}

.choices__list--dropdown .choices__list {
  position: relative;
  max-height: 300px;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
  will-change: scroll-position;
}

.choices__list--dropdown .choices__item {
  position: relative;
  padding: 10px;
  font-size: 14px;
}

[dir="rtl"] .choices__list--dropdown .choices__item {
  text-align: right;
}

@media (min-width: 640px) {
  .choices__list--dropdown .choices__item--selectable {
    padding-right: 100px;
  }
  .choices__list--dropdown .choices__item--selectable:after {
    content: attr(data-select-text);
    font-size: 12px;
    opacity: 0;
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
  }
  [dir="rtl"] .choices__list--dropdown .choices__item--selectable {
    text-align: right;
    padding-left: 100px;
    padding-right: 10px;
  }
  [dir="rtl"] .choices__list--dropdown .choices__item--selectable:after {
    right: auto;
    left: 10px;
  }
}

.choices__list--dropdown .choices__item--selectable.is-highlighted {
  background-color: #f2f2f2;
}

.choices__list--dropdown .choices__item--selectable.is-highlighted:after {
  opacity: .5;
}

.choices__item {
  cursor: default;
}

.choices__item--selectable {
  cursor: pointer;
}

.choices__item--disabled {
  cursor: not-allowed;
  -webkit-user-select: none;
     -moz-user-select: none;
      -ms-user-select: none;
          user-select: none;
  opacity: .5;
}

.choices__heading {
  font-weight: 600;
  font-size: 12px;
  padding: 10px;
  border-bottom: 1px solid #f7f7f7;
  color: gray;
}

.choices__button {
  text-indent: -9999px;
  -webkit-appearance: none;
  -moz-appearance: none;
       appearance: none;
  border: 0;
  background-color: transparent;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
}

.choices__button:focus {
  outline: none;
}

.choices__input {
  display: inline-block;
  vertical-align: baseline;
  background-color: #f9f9f9;
  font-size: 14px;
  margin-bottom: 5px;
  border: 0;
  border-radius: 0;
  max-width: 100%;
  padding: 4px 0 4px 2px;
}

.choices__input:focus {
  outline: 0;
}

[dir="rtl"] .choices__input {
  padding-right: 2px;
  padding-left: 0;
}

.choices__placeholder {
  opacity: .5;
}

/*=====  End of Choices  ======*/
* {
  box-sizing: border-box;
}


.s009 {
  height: calc(100vh - 48.8px) !important;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: center;
      justify-content: center;
  -ms-flex-align: center;
  background: #d9eff5;
  padding: 15px;
  font-family: 'Lato', sans-serif;
}

.s009 form {
  display: block;
  margin-top: 100px !important;
  width: 100%;
  max-width: 900px;
  margin: 0;
}

.s009 form .inner-form {
  // width: 100%;
}

.s009 form .inner-form .input-field {
  position: relative;
}

.s009 form .inner-form .input-field input {
  height: 100%;
  border: 0;
  background: #fff;
  display: block;
  width: 100%;
  padding: 10px 32px 10px 70px;
  font-size: 18px;
  color: #666;
  border-radius: 3px;
  height: 70px;
  color: #555;
  font-family: 'Lato', sans-serif;
}

.s009 form .inner-form .input-field input.placeholder {
  color: #999;
  font-size: 18px;
  font-weight: 600;
}

.s009 form .inner-form .input-field input:-moz-placeholder {
  color: #999;
  font-size: 18px;
  font-weight: 600;
}

.s009 form .inner-form .input-field input::-webkit-input-placeholder {
  color: #999;
  font-size: 18px;
  font-weight: 600;
}

.s009 form .inner-form .input-field input:hover, .s009 form .inner-form .input-field input:focus {
  box-shadow: none;
  outline: 0;
}
.btn-import {
  background-color: rgb(2, 170, 2) !important;
  border: none !important;
}
.btn-redirect:hover {
border-color: green !important;
color: green !important;
}
.btn-import:hover {
  background-color: green !important;
  border: none !important;
}

.s009 form .inner-form .input-field .btn-crawl {
  min-width: 100px;
  height: 40px;
  padding: 0 15px;
  background: rgb(2, 202, 2);
  white-space: nowrap;
  border-radius: 0;
  font-size: 14px;
  margin-right: 20px;
  color: #fff;
  transition: all .2s ease-out, color .2s ease-out;
  border: 0;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.15);
}

.s009 form .inner-form .input-field .btn-crawl:hover, .s009 form .inner-form .input-field .btn-crawl:focus {
  background: green;
}

.s009 form .inner-form .input-field .btn-delete {
  min-width: 100px;
  height: 40px;
  padding: 0 15px;
  background: transparent;
  white-space: nowrap;
  border-radius: 0;
  font-size: 14px;
  color: #666;
  transition: all .2s ease-out, color .2s ease-out;
  border: 0;
  cursor: pointer;
  font-weight: bold;
}

.s009 form .inner-form .input-field .btn-delete:hover, .s009 form .inner-form .input-field .btn-delete:focus {
  color: #000;
  outline: 0;
  box-shadow: none;
}

.s009 form .inner-form .basic-search {
  /* box-shadow: 0px 8px 20px 0px rgba(0, 0, 0, 0.15); */
  /* border-bottom: 2px solid rgb(4, 250, 4); */
  background-color: white !important;
  padding: 30px 0px 20px 15px;
}

.s009 form .inner-form .basic-search .input-field {
  width: 100%;
}

.s009 form .inner-form .basic-search .input-field input {
  padding: 10px 80px 10px 40px;
  font-family: 'Lato', sans-serif;
}

.s009 form .inner-form .advance-search {
  background: #fff;
  padding: 40px;
  /* box-shadow: 0px 8px 20px 0px rgba(0, 0, 0, 0.15); */
}

.s009 form .inner-form .advance-search .desc {
  font-size: 14px;
  color: #999;
  display: block;
  margin-bottom: 26px;
  font-weight: bold;
}

.s009 form .inner-form .advance-search .row {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: justify;
      justify-content: space-between;
  -ms-flex-align: center;
      align-items: center;
  margin-bottom: 20px;
}

.s009 form .inner-form .advance-search .row.second {
  margin-bottom: 46px;
}

.s009 form .inner-form .advance-search .row.third {
  margin-bottom: 0;
}
.crawl-choice-field {
  width: 250px; 
  min-width: 150px; 
  margin: 5px 15px 15px 15px; 
  align-self: center;
}
.s009 form .inner-form .advance-search .row.third .input-field {
  width: 100%;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: justify;
      justify-content: space-between;
  -ms-flex-align: center;
      align-items: center;
}

.s009 form .inner-form .advance-search .row.third .input-field .result-count {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-pack: start;
      justify-content: flex-start;
  -ms-flex-align: center;
      align-items: center;
  width: 110px;
  color: #666;
  font-size: 14px;
}

.s009 form .inner-form .advance-search .row.third .input-field .result-count span {
  color: rgb(4, 250, 4);
  padding-right: 5px;
}

.s009 form .inner-form .advance-search .input-field {
  width: calc((100% - 40px) / 3);
}

.s009 form .inner-form .advance-search .input-select {
  height:40px;
  background-color: #00a156;
}

.s009 form .inner-form .advance-search .input-select1 {
  width: calc((100% - 40px) / 3);
  height:40px;
  font-family: 'Lato', sans-serif;
}

.s009 form .inner-form .advance-search .choices__inner {
  background: transparent;
  border-radius: 0;
  border: 0;
  border: 1px solid rgba(0, 0, 0, 0.1);
  height: 100%;
  color: #fff;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
      align-items: center;
  padding: 0;
  padding-right: 30px;
  font-size: 14px;
  min-height: 40px;
}

.s009 form .inner-form .advance-search .choices__inner .choices__list.choices__list--single {
  display: -ms-flexbox;
  display: flex;
  padding: 5px 18px;
  -ms-flex-align: center;
      align-items: center;
  height: 100%;
}

.s009 form .inner-form .advance-search .choices__inner .choices__item.choices__item--selectable.choices__placeholder {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
      align-items: center;
  height: 100%;
  opacity: 1;
  color: #666;
  font-weight: bold;
}

.s009 form .inner-form .advance-search .choices__inner .choices__list--single .choices__item {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
      align-items: center;
  height: 100%;
  color: rgb(4, 250, 4);
  font-weight: bold;
}

.s009 form .inner-form .advance-search .choices__list.choices__list--dropdown {
  border: 0;
  background: #fff;
  padding: 10px 18px 20px 18px;
  margin-top: 0;
  border-radius: 0;
  box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.15);
}

.s009 form .inner-form .advance-search .choices__list.choices__list--dropdown .choices__item--selectable {
  padding-right: 0;
}

.s009 form .inner-form .advance-search .choices__list--dropdown .choices__item--selectable.is-highlighted {
  background: transparent;
  color: rgb(4, 250, 4);
}

.s009 form .inner-form .advance-search .choices__list--dropdown .choices__item {
  color: #666;
  min-height: 20px;
  padding: 8px 0;
  font-weight: bold;
}

.s009 form .inner-form .advance-search .choices[data-type*="select-one"]:after {
  border: 0;
  width: 32px;
  height: 32px;
  margin: 0;
  transform: none;
  opacity: 1;
  right: 15px;
  top: 6px;
  background-size: 18px 18px;
  background-position: right center;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg fill='%23999' xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3e%3cpath d='M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
}

.s009 form .inner-form .advance-search .choices[data-type*="select-one"].is-open {
  box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.1);
}

.s009 form .inner-form .advance-search .choices[data-type*="select-one"].is-open:after {
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg fill='%23999' xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3e%3cpath d='M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z'/%3e%3c/svg%3e");
}

.s009 form .inner-form .advance-search .choices[data-type*="select-one"] .choices__button {
  display: none;
  -webkit-user-select: none;
     -moz-user-select: none;
      -ms-user-select: none;
          user-select: none;
}

@media screen and (max-width: 767px) {
  .s009 form .inner-form .basic-search .input-field input {
    padding: 10px 80px 10px 15px;
  }
  .s009 form .inner-form .advance-search {
    padding: 30px 15px;
  }
  .s009 form .inner-form .advance-search .row {
    display: block;
  }
  .s009 form .inner-form .advance-search .input-field {
    width: 100%;
    margin-bottom: 20px;
  }
}

/* Style the tab */
.tab {
  overflow: hidden;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}

/* Style the buttons that are used to open the tab content */
.tab button {
  background-color: inherit;
  float: left;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 14px 16px;
  transition: 0.3s;
}

/* Change background color of buttons on hover */
.tab button:hover {
  background-color: #ddd;
}

/* Create an active/current tablink class */
.tab button.active {
  background-color: #ccc;
}

/* Style the tab content */
.tabcontent {
  display: none;
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-top: none;
}
</style>
<style>
    @import "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css";
</style>




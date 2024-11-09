<template>
  <div style="background-color: #d9eff5">
    <section class="welcome p-t-10">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <h1 class="title-4">Dashboard</h1>
            <hr class="line-seprate" />
          </div>
        </div>
      </div>
    </section>
    <!-- STATISTIC-->
    <section class="statistic statistic2">
      <div class="container">
        <div class="row">
          <div class="col-md-6 col-lg-3">
            <div class="statistic__item statistic__item--green">
              <h2 class="number">{{ SumaryDBData.total_node }}</h2>
              <span class="desc">Nodes</span>
              <div class="icon">
                <i class="zmdi zmdi-account-o"></i>
              </div>
            </div>
          </div>
          <div class="col-md-6 col-lg-3">
            <div class="statistic__item statistic__item--orange">
              <h2 class="number">{{ SumaryDBData.total_relation }}</h2>
              <span class="desc">Relations</span>
              <div class="icon">
                <i class="zmdi zmdi-shopping-cart"></i>
              </div>
            </div>
          </div>
          <div class="col-md-6 col-lg-3">
            <div class="statistic__item statistic__item--blue">
              <h2 class="number">{{ SumaryDBData.total_course }}</h2>
              <span class="desc">Course</span>
              <div class="icon">
                <i class="zmdi zmdi-calendar-note"></i>
              </div>
            </div>
          </div>
          <div class="col-md-6 col-lg-3">
            <div class="statistic__item statistic__item--red">
              <h2 class="number">{{ SumaryDBData.total_career }}</h2>
              <span class="desc">Careers</span>
              <div class="icon">
                <i class="zmdi zmdi-money"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- END STATISTIC-->

    <!-- STATISTIC CHART-->
    <section class="statistic-chart">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <h3 class="title-5 m-b-35">statistics</h3>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6 col-lg-4">
            <div class="statistic-chart-1">
              <h3 class="title-3 m-b-30">Top Skills By Subject</h3>
              <div class="table-responsive">
                <table class="table table-top-campaign">
                  <tbody>
                    <tr
                      v-for="td in SumaryDBData.subject_topskill"
                      :key="td.subject"
                    >
                      <td>{{ td.subject }}</td>
                      <td v-for="skill in td.topskill" v-bind:key="skill">
                        {{ skill.name }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div class="col-md-6 col-lg-4">
            <div class="top-campaign">
              <h3 class="title-3 m-b-30">Total courses in website</h3>
              <div class="table-responsive">
                <table class="table table-top-campaign">
                  <tbody>
                    <tr v-for="td in SumaryDBData.web_course" :key="td.webName">
                      <td>{{ td.webName }}</td>
                      <td>{{ td.numberCrs }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div class="col-md-6 col-lg-4">
            <div class="top-campaign">
              <h3 class="title-3 m-b-30">Number of nodes</h3>
              <div class="table-responsive">
                <table class="table table-top-campaign">
                  <tbody>
                    <tr v-for="td in SumaryDBData.numberofnode" :key="td.node">
                      <td>{{ td.node }}</td>
                      <td>{{ td.number }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <!-- <div class="chart-percent-2">
                                <h3 class="title-3 m-b-30">Export Data</h3>
                                <div class="chart-wrap">
                                        <treeselect style="width: 90%; margin-left: auto; margin-right: auto; align-self: center;"
                                            :multiple="false"
                                            :options="TypeExportData"
                                            v-model="valueTypeExportData"
                                            placeholder="Choose data to export"
                                            v-on:input="GetDataToExport"
                                            v-on:select="GetDataToExport"
                                            v-on:deselect="GetDataToExport"
                                            v-on:close="GetDataToExport"
                                        />
                                        <br>
                                        <b-button variant="success" style="display: block;margin-left:auto; margin-right:auto; width:90%;">
                                        <vue-blob-json-csv
                                            @success="handleSuccess"
                                            @error="handleError"
                                            file-type="json"
                                            v-bind:file-name="filename"
                                            title="Download as JSON File"
                                            :data="ExportData"
                                            confirm="Do you want to download it?"
                                        ></vue-blob-json-csv>
                                        </b-button>
                                        <b-button variant="success" style="display: block;margin-left:auto; margin-right:auto; margin-top: 5px; width:90%;">
                                        <download-csv
                                            v-bind:name="filenamecsv"
                                            :data  = "ExportData">
                                            Download as CSV File
                                        </download-csv>
                                        </b-button>
                                </div>
                            </div> -->
          </div>
        </div>
      </div>
    </section>
    <!-- END STATISTIC CHART-->

    <!-- DATA TABLE-->
    <section class="p-t-20">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <h3 class="title-5 m-b-35">Course</h3>
            <div class="table-data__tool">
              <div class="table-data__tool-left">
                <div class="rs-select2--light rs-select2--md">
                  <treeselect
                    style="width: 130px; align-self: center"
                    :multiple="false"
                    :options="[
                      { id: 1, label: 1 },
                      { id: 2, label: 2 },
                    ]"
                    v-model="valueRangeScore"
                    placeholder="Options"
                    v-on:input="filterColumn"
                    v-on:select="filterColumn"
                    v-on:deselect="filterColumn"
                    v-on:close="filterColumn"
                  />
                  <div class="dropDownSelect2"></div>
                </div>
                <div class="rs-select2--light rs-select2--sm">
                  <treeselect
                    style="width: 130px; align-self: center"
                    :multiple="false"
                    :options="[
                      { id: 1, label: 'Today' },
                      { id: 2, label: '3 Days' },
                      { id: 3, label: '1 Week' },
                    ]"
                    v-model="valueRangeScore"
                    placeholder="Today"
                    v-on:input="filterColumn"
                    v-on:select="filterColumn"
                    v-on:deselect="filterColumn"
                    v-on:close="filterColumn"
                  />
                </div>
              </div>
              <div class="table-data__tool-right">
                <input
                  type="search"
                  class="input px:width-25"
                  placeholder="Search here..."
                  v-model="searchInput"
                  @keyup="searchEvent()"
                />
                <i class="fa fa-search"></i>
                <b-button variant="success" @click="showExportData = true"
                  >Export Data
                </b-button>
              </div>
            </div>
          </div>
        </div>
        <a-table
          bordered
          :data-source="currentData"
          :row-selection="rowSelection"
        >
          <a-table-column
            key="crsName"
            title="Course Name"
            data-index="crsName"
          />
          <a-table-column
            key="website"
            title="Website"
            data-index="website"
            :filters="[
              { text: 'Coursera', value: 'coursera.org' },
              { text: 'Udemy', value: 'udemy.com' },
              { text: 'Edx', value: 'edx.org' },
            ]"
            @filter="(value) => filterWebsite(value)"
          />
          <a-table-column key="crsFee" title="Fee" data-index="crsFee" />
          <a-table-column key="crsTime" title="Time" data-index="crsTime" />
          <a-table-column
            key="crsEnroll"
            title="Enroll"
            data-index="crsEnroll"
          />
          <a-table-column
            key="crsRating"
            title="Rating"
            data-index="crsRating"
          />
          <a-table-column
            key="instructor"
            title="Instructor"
            data-index="instructor"
          />
          <a-table-column
            key="organization"
            title="Organization"
            data-index="organization"
          />
          <a-table-column key="program" title="Program" data-index="program" />
          <a-table-column
            key="subtitle"
            title="Subtitle"
            data-index="subtitle"
          />
          <!-- <a-table-column-group>
                <span slot="title" style="color: #1890ff">Teach Skill</span>
                <a-table-column key="knowledge" data-index="knowledge">
                    <span slot="title" style="color: #1890ff">Knowledge</span>
                </a-table-column>
                <a-table-column key="tool" data-index="tool">
                    <span slot="title" style="color: #1890ff">Tool</span>
                </a-table-column>
                </a-table-column-group> -->
          <a-table-column key="action" title="Action">
            <template slot-scope="text, record">
              <span>
                <b-button
                  @click="(showTeachSkill = true), custom(record)"
                  class="btn btn-info btn-sm"
                  style="
                    width: 100px;
                    background-color: white;
                    border: 2px solid rgb(4, 250, 4);
                    color: rgb(4, 250, 4);
                    font-weight: bold;
                  "
                >
                  Teach Skill
                </b-button>
                <br />
                <b-button
                  @click="(showRequireSkill = true), custom(record)"
                  class="btn btn-info btn-sm"
                  style="
                    width: 100px;
                    margin-top: 5px;
                    background-color: white;
                    border: 2px solid rgb(4, 250, 4);
                    color: rgb(4, 250, 4);
                    font-weight: bold;
                  "
                >
                  Require Skill</b-button
                >
              </span>
            </template>
          </a-table-column>
        </a-table>
      </div>
    </section>

    <!-- END DATA TABLE-->
    <a-modal
      v-model="showExportData"
      title="Export Data"
      style="margin-top: 180px"
      :ok-button-props="{ style: { display: 'none' } }"
      :cancel-button-props="{ style: { display: 'none' } }"
    >
      <div class="chart-wrap">
        <treeselect
          style="
            width: 90%;
            margin-left: auto;
            margin-right: auto;
            align-self: center;
          "
          :multiple="false"
          :options="TypeExportData"
          v-model="valueTypeExportData"
          placeholder="Choose data to export"
          v-on:input="GetDataToExport"
          v-on:select="GetDataToExport"
          v-on:deselect="GetDataToExport"
          v-on:close="GetDataToExport"
        />
        <br />
        <b-button
          variant="success"
          style="
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 90%;
          "
        >
          <vue-blob-json-csv
            @success="handleSuccess"
            @error="handleError"
            file-type="json"
            v-bind:file-name="filename"
            title="Download as JSON File"
            :data="ExportData"
            confirm="Do you want to download it?"
          ></vue-blob-json-csv>
        </b-button>
        <b-button
          variant="success"
          style="
            display: block;
            margin-left: auto;
            margin-right: auto;
            margin-top: 5px;
            width: 90%;
          "
        >
          <download-csv v-bind:name="filenamecsv" :data="ExportData">
            Download as CSV File
          </download-csv>
        </b-button>
      </div>
    </a-modal>
    <a-modal
      v-model="showTeachSkill"
      title="What you will learn"
      style="margin-top: 180px"
      :ok-button-props="{ style: { display: 'none' } }"
    >
      <p style="font-size: medium" v-bind:value="teachskill">
        Which skill you will learn in this course including:
      </p>
      <ul style="font-size: medium" v-if="teachskill.knowledge != '[]'">
        Knowledge
        <li
          style="font-size: medium"
          v-for="skill in teachskill.knowledge"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul style="font-size: medium" v-if="teachskill.tool != '[]'">
        Tool
        <li
          style="font-size: medium"
          v-for="skill in teachskill.tool"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul
        style="font-size: medium"
        v-if="teachskill.programinglanguage != '[]'"
      >
        Programing Language
        <li
          style="font-size: medium"
          v-for="skill in teachskill.programinglanguage"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul style="font-size: medium" v-if="teachskill.platform != '[]'">
        Platform
        <li
          style="font-size: medium"
          v-for="skill in teachskill.platform"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul style="font-size: medium" v-if="teachskill.framework != '[]'">
        Framework
        <li
          style="font-size: medium"
          v-for="skill in teachskill.framework"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
    </a-modal>
    <a-modal
      v-model="showRequireSkill"
      title="Require"
      style="margin-top: 180px"
      :ok-button-props="{ style: { display: 'none' } }"
    >
      <p style="font-size: medium" v-bind:value="requireskill">
        Which skill you need to know before enroll this course including:
      </p>
      <ul
        style="font-size: medium"
        v-if="requireskill.require_knowledge != null"
      >
        Knowledge
        <li
          style="font-size: medium"
          v-for="skill in requireskill.require_knowledge"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul style="font-size: medium" v-if="requireskill.require_tool != null">
        Tool
        <li
          style="font-size: medium"
          v-for="skill in requireskill.require_tool"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul
        style="font-size: medium"
        v-if="requireskill.require_programinglanguage != null"
      >
        Programing Language
        <li
          style="font-size: medium"
          v-for="skill in requireskill.require_programinglanguage"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul
        style="font-size: medium"
        v-if="requireskill.require_platform != null"
      >
        Platform
        <li
          style="font-size: medium"
          v-for="skill in requireskill.require_platform"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
      <ul
        style="font-size: medium"
        v-if="requireskill.require_framework != null"
      >
        Framework
        <li
          style="font-size: medium"
          v-for="skill in requireskill.require_framework"
          v-bind:key="skill"
        >
          {{ skill }}
        </li>
      </ul>
    </a-modal>
  </div>
</template>

<script>
import { $array } from "alga-js";
import axios from "axios";
import Treeselect from "vue3-treeselect";

export default {
  name: "Dashboard",
  props: {},
  data() {
    return {
      showTeachSkill: false,
      showRequireSkill: false,
      showExportData: false,
      teachskill: "",
      requireskill: "",
      aaaa: "",
      filterData: [],
      show: false,
      searchEntries: [],
      currentData: [],
      columns: [
        {
          title: "Course Name",
          dataIndex: "crsName",
          key: "crsName",
        },
        {
          title: "Website",
          dataIndex: "website",
          key: "website",
        },
        {
          title: "Fee",
          dataIndex: "crsFee",
          key: "crsFee",
        },
        {
          title: "Time",
          dataIndex: "crsTime",
          key: "crsTime",
        },
        {
          title: "Enroll",
          dataIndex: "crsEnroll",
          key: "crsEnroll",
        },
        {
          title: "Rating",
          dataIndex: "crsRating",
          key: "crsRating",
        },
        {
          title: "Instructor",
          dataIndex: "instructor",
          key: "instructor",
        },
        {
          title: "Organization",
          dataIndex: "organization",
          key: "organization",
        },
        {
          title: "Program",
          dataIndex: "program",
          key: "program",
        },
        {
          title: "Subtitle",
          dataIndex: "subtitle",
          key: "subtitle",
        },
      ],
      sumarydb: {
        total_node: 0,
        total_relation: 0,
        total_course: 0,
        total_career: 0,
        total_knowledge: 0,
        total_plaform: 0,
        total_framework: 0,
        total_language: 0,
        total_tool: 0,
        total_task: 0,
        total_level: 0,
        total_web: 0,
        total_instructor: 0,
        web_course: [],
        subject_topskill: [],
      },
      selected: ["coursera"],
      Domain: [
        { id: "coursera", label: "Coursera" },
        { id: "udemy", label: "Udemy" },
        { id: "edx", label: "Edx" },
        { id: "ed2go", label: "Ed2go" },
        { id: "udacity", label: "Udacity" },
      ],
      filename: "career",
      filenamecsv: "course",
      TypeExportData: [
        { id: "all", label: "All data available in database" },
        { id: "course", label: "All data about course" },
        { id: "career", label: "All data about career" },
        { id: "table", label: "Data in table" },
      ],
      TypeExport: [
        { id: "json", label: "JSON File" },
        { id: "csv", label: "CSV File" },
      ],
      ExportData: [
        { id: "coursera", label: "Coursera" },
        { id: "udemy", label: "Udemy" },
        { id: "edx", label: "Edx" },
        { id: "ed2go", label: "Ed2go" },
        { id: "udacity", label: "Udacity" },
      ],
      infoCourse: [],
      infoCareer: [],
    };
  },
  components: {
    Treeselect,
  },
  created() {
    let today = new Date();
    localStorage.setItem("time_crawl", today.toString())
    console.log("aaa", localStorage.getItem("time_crawl"))
    axios
      .get(`api/get_sumarydb/`)
      .then((response) => {
        this.sumarydb = JSON.parse(response.data);
      })
      .catch((e) => {
        this.errors.push(e);
      });
    axios
      .get(`api/get_data_course/`)
      .then((response) => {
        this.infoCourse = response.data;
        this.currentData = response.data.map(value=> {
          value.subtitle = value.subtitle.toString().replaceAll(",",", ");
          value.organization = value.organization.toString().replaceAll(",",", ");
          value.instructor = value.instructor.toString().replaceAll(",",", ");
          value.level = value.level.toString().replaceAll(",",", ");
          value.program = value.program.toString().replaceAll(",",", ");
          
          value.website = value.website.toString().replace("www.", "");
          let result = value.website.slice(0, value.website.indexOf("."));
          value.website = result.charAt(0).toUpperCase() + result.slice(1);
          return value;
        })
      })
      .catch((e) => {
        this.errors.push(e);
      });
    axios
      .get(`api/get_data_career/`)
      .then((response) => {
        this.infoCareer = response.data;
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
  computed: {
    SumaryDBData() {
      return this.sumarydb;
    },
    rowSelection() {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          console.log(
            `selectedRowKeys: ${selectedRowKeys}`,
            "selectedRows: ",
            selectedRows
          );
        },
        getCheckboxProps: (record) => ({
          props: {
            disabled: record.name === "Disabled User", // Column configuration not to be checked
            name: record.name,
          },
        }),
      };
    },
  },
  methods: {
    async onClickCrawl() {
      console.log("AAA:", this.type);
      console.log(this.valueCategory);
      await axios
        .post(`api/crawl_train/`, {
          type: this.type,
          linkcrawl: this.linkcrawl,
          category: this.valueCategory,
          domain: this.valueDomain,
          depth: this.valueDepth,
        })
        .then((result) => {
          console.log("True");
          this.$router.push({
            name: "NER",
            params: { train_output: JSON.parse(result.data)["train_output"] },
          });
        })
        .catch((err) => {
          console.log(err);
          this.showLoading = false;
          alert("Crawl process fail!");
        });
    },
    GetDataToExport() {
      if (this.valueTypeExportData === "course") {
        this.ExportData = this.infoCourse;
        this.filename = "course";
        this.filenamecsv = "course.csv";
      }
      if (this.valueTypeExportData === "career") {
        this.ExportData = this.infoCareer;
        this.filename = "career";
        this.filenamecsv = "career.csv";
      }
      if (this.valueTypeExportData === "table") {
        this.ExportData = this.currentData;
        this.filename = "datatable";
        this.filenamecsv = "datatable.csv";
      }
    },
    custom(record) {
      this.teachskill = record;
      this.requireskill = record;
    },
    toggleSelectedTags(oldTags, tag, checked) {
      let newTags = [...oldTags];
      if (checked) {
        newTags.push(tag);
      } else {
        newTags = newTags.filter((t) => t != tag);
      }
      return newTags;
    },
    filterWebsite(value) {
      console.log(this.aaaa);
      console.log(value);
      for (let j in this.infoCourse) {
        if (this.infoCourse[j].website === value) {
          this.filterData.push(this.infoCourse[j]);
        }
      }
      console.log(this.filterData);
      this.infoCourse = this.filterData;
    },
    searchEvent() {
      console.log(this.searchInput);
      if (this.searchInput.length >= 3) {
        console.log(this.searchInput);
        this.searchEntries = $array.search(this.infoCourse, this.searchInput);
        this.currentData = this.searchEntries;
      } else {
        this.searchEntries = [];
        this.currentData = this.infoCourse;
      }
    },
  },
};
</script>

<style lang="scss">
@import "../assets/cooladmin/vendor/font-awesome-4.7/css/font-awesome.min.css";
@import "../assets/cooladmin/vendor/font-awesome-5/css/fontawesome-all.min.css";
@import "../assets/cooladmin/vendor/mdi-font/css/material-design-iconic-font.min.css";
@import "../assets/cooladmin/vendor/bootstrap-4.1/bootstrap.min.css";
@import "../assets/cooladmin/vendor/animsition/animsition.min.css";
@import "../assets/cooladmin/vendor/bootstrap-progressbar/bootstrap-progressbar-3.3.4.min.css";
@import "../assets/cooladmin/vendor/wow/animate.css";
@import "../assets/cooladmin/vendor/css-hamburgers/hamburgers.min.css";
@import "../assets/cooladmin/vendor/slick/slick.css";
@import "../assets/cooladmin/vendor/select2/select2.min.css";
@import "../assets/cooladmin/vendor/perfect-scrollbar/perfect-scrollbar.css";
@import "../assets/cooladmin/css/theme.css";
</style>
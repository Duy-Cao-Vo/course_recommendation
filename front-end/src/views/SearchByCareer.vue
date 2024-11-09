<template>
  <div>
    <ListFreeCourses
      :topFreeCourse="topFreeCourses"
      :topFreeLoad="freeCourseLoading"
    />
    <AllListPopularCourse
      defaltTabtitle="All"
      :popularCoursesOfAll="popularCoursesOfAll"
      :loadingCardOfAll="loadingCardOfAll"
      :numberList="0"
    />
    <PopularTopics />
    <a-row
      type="flex"
      justify="center"
      class="search-mobile-screen"
      style="margin-bottom: 15px"
    >
      <a-col :sm="24" :lg="20" :xl="18">
        <span class="large-title">Course Catalog </span>
      </a-col>
    </a-row>
    <a-row type="flex" class="justify-screen search-mobile-screen">
      <a-row
        type="flex"
        justify="center"
        class="search-mobile-screen"
        style="margin-bottom: 10px"
      >
      </a-row>
      <a-col :xs="8" :lg="4" class="search-screen max-mobile-screen">
        <a-menu
          class="filter-bar"
          style="width: 100%"
          :default-selected-keys="['1']"
          mode="inline"
        >
          <a-menu-item
            class="btn-title-skill"
            key="Career"
            @click="showModalCareer"
          >
            Career
          </a-menu-item>
          <a-menu-item
            class="btn-title-skill"
            key="Knowledges"
            @click="showModalKnowledge"
          >
            Knowledge
          </a-menu-item>
          <a-menu-item
            class="btn-title-skill"
            key="platfrom"
            @click="showModalPlatfrom"
          >
            Platform
          </a-menu-item>
          <a-menu-item
            class="btn-title-skill"
            key="tool"
            @click="showModalTool"
          >
            Tool
          </a-menu-item>
          <a-menu-item
            class="btn-title-skill"
            key="language"
            @click="showModalLanguage"
          >
            Program Language
          </a-menu-item>
          <a-menu-item
            class="btn-title-skill"
            key="framework"
            @click="showModalFramework"
          >
            Framework
          </a-menu-item>
        </a-menu>
      </a-col>
      <a-col
        :xs="16"
        :lg="{ offset: 0, span: 16 }"
        :xl="{ offset: 0, span: 12 }"
        class="search-screen max-mobile-screen"
      >
        <div v-if="!this.loadingCourse">
          <div v-if="courses.length != 0">
            <a-select
              show-search
              placeholder="Select website"
              option-filter-prop="children"
              style="
                top: -12px;
                width: 200px;
                float: right !important;
                margin-top: 9px;
              "
              :filter-option="filterOption"
              @change="selectWeb"
              default-value="All"
            >
              <a-select-option
                v-for="value in webs"
                :key="value"
                :value="value"
              >
                {{ value }}
              </a-select-option>
            </a-select>
            <h5
              style="
                color: rgb(2, 160, 2) !important;
                overflow: hidden;
                max-height: 100px;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
              "
            >
              {{ courses.length }} results
              <span v-if="!isEmpty"> for {{ this.lastCareer }}</span
              ><span v-if="listSearch.length > 0">
                with
                <span style="text-transform: capitalize">{{
                  listSearch
                }}</span></span
              >
            </h5>
            <CourseDetail
              v-for="course in displayCourse"
              v-bind:key="course.id"
              v-bind:courseDetail="course"
              style="margin-bottom: 10px"
            />
          </div>
          <div v-else>
            <h2 style="color: rgb(112, 112, 112) !important; font-weight: 700">
              Sorry, we couldn't find any matching results
            </h2>
          </div>
        </div>
        <div v-else>
          <a-card
            :loading="true"
            style="height: 160px !important; min-height: 160px !important"
          >
            whatever content
          </a-card>
        </div>
      </a-col>
    </a-row>
    <a-modal
      id="career-modal"
      class="show-skill"
      :visible="showCareer"
      @cancel="handleCancel"
      :closable="false"
      :maskClosable="false"
    >
      <template v-slot:title>
        <div class="skill-header">
          <p style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px">
            Career
          </p>
          <div style="display: flex">
            <a-button
              style="margin-left: 10px"
              class="btn-reset"
              @click="
                () => {
                  this.chosenCareer = '';
                  this.notifyReset();
                }
              "
              >Reset</a-button
            >
            <a-input
              @change="(event) => (this.careerSearch = event.target.value)"
              style="max-width: 200px; margin-left: 5px"
              placeholder="Search career"
            />
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <a-button
          class="btn-cancel"
          @click="
            () => {
              handleCancel();
              this.onCancelCareer();
            }
          "
          >Cancel</a-button
        >
        <a-button
          class="btn-confirm"
          @click="
            () => {
              handleCancel();
              this.onConfirmCareer();
            }
          "
          >Confirm</a-button
        >
      </template>

      <a-radio-group
        :options="displayCareer"
        :value="chosenCareer"
        @change="onChooseCareer"
      />
    </a-modal>
    <a-modal
      id="knowledge-modal"
      class="show-skill"
      :visible="showKnowledge"
      @cancel="handleCancel"
      :closable="false"
      :maskClosable="false"
    >
      <template v-slot:title>
        <div class="skill-header">
          <p style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px">
            Knowledge
          </p>
          <div class="small-flex" style="display: flex">
            <a-button
              style="margin-left: 10px"
              class="btn-reset"
              @click="
                () => {
                  this.checkedKnowledges = [];
                  this.notifyReset();
                }
              "
              >Reset</a-button
            >
            <a-input
              @change="(event) => (this.knowledgeSearch = event.target.value)"
              style="max-width: 200px; margin-left: 5px"
              placeholder="Search knowledge"
            />
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <a-button
          class="btn-cancel"
          @click="
            () => {
              handleCancel();
              this.checkedKnowledges = this.searchKnowledges;
            }
          "
          >Cancel</a-button
        >
        <a-button
          class="btn-confirm"
          @click="
            () => {
              handleCancel();
              this.searchKnowledges = this.checkedKnowledges;
              this.searchFrameworks = [];
              this.searchPlatforms = [];
              this.searchTools = [];
              this.searchPrograminglanguages = [];
              this.checkedPlatforms = [];
              this.checkedTools = [];
              this.checkedPrograminglanguages = [];
              this.checkedFrameworks = [];
              onClickSearch();
            }
          "
          >Confirm</a-button
        >
      </template>
      <a-checkbox-group
        :options="this.displayKnowledge"
        :value="this.checkedKnowledges"
        @change="onChangeKnowledge"
      />
    </a-modal>

    <a-modal
      class="show-skill"
      :visible="showPlatform"
      @cancel="handleCancel"
      :closable="false"
      :maskClosable="false"
    >
      <template v-slot:title>
        <div class="skill-header">
          <p style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px">
            Platform
          </p>
          <div class="small-flex" style="display: flex">
            <a-button
              style="margin-left: 10px"
              class="btn-reset"
              @click="
                () => {
                  this.checkedPlatforms = [];
                  this.notifyReset();
                }
              "
              >Reset</a-button
            >
            <a-input
              @change="(event) => (this.platformSearch = event.target.value)"
              style="max-width: 200px; margin-left: 5px"
              placeholder="Search platform"
            />
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <a-button
          class="btn-cancel"
          @click="
            () => {
              handleCancel();
              this.checkedPlatforms = this.searchPlatforms;
            }
          "
          >Cancel</a-button
        >
        <a-button
          class="btn-confirm"
          @click="
            () => {
              handleCancel();
              this.searchPlatforms = this.checkedPlatforms;
              this.searchFrameworks = [];
              this.searchKnowledges = [];
              this.searchTools = [];
              this.searchPrograminglanguages = [];
              this.checkedKnowledges = [];
              this.checkedTools = [];
              this.checkedPrograminglanguages = [];
              this.checkedFrameworks = [];
              onClickSearch();
            }
          "
          >Confirm</a-button
        >
      </template>
      <a-checkbox-group
        :options="displayPlatfrom"
        :value="this.checkedPlatforms"
        @change="onChangePlatforms"
      />
    </a-modal>

    <a-modal
      class="show-skill"
      :visible="showTool"
      :closable="false"
      :maskClosable="false"
    >
      <template v-slot:title>
        <div class="skill-header">
          <p style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px">
            Tool
          </p>
          <div class="small-flex" style="display: flex">
            <a-button
              style="margin-left: 10px"
              class="btn-reset"
              @click="
                () => {
                  this.checkedTools = [];
                  this.notifyReset();
                }
              "
              >Reset</a-button
            >
            <a-input
              @change="(event) => (this.toolSearch = event.target.value)"
              style="max-width: 200px; margin-left: 5px"
              placeholder="Search tool"
            />
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <a-button
          class="btn-cancel"
          @click="
            () => {
              handleCancel();
              this.checkedTools = this.searchTools;
            }
          "
          >Cancel</a-button
        >
        <a-button
          class="btn-confirm"
          @click="
            () => {
              handleCancel();
              this.searchTools = this.checkedTools;
              this.searchFrameworks = [];
              this.searchKnowledges = [];
              this.searchPlatforms = [];
              this.searchPrograminglanguages = [];
              this.checkedKnowledges = [];
              this.checkedPlatforms = [];
              this.checkedPrograminglanguages = [];
              this.checkedFrameworks = [];
              onClickSearch();
            }
          "
          >Confirm</a-button
        >
      </template>
      <a-checkbox-group
        :options="displayTool"
        :value="this.checkedTools"
        @change="onChangeTools"
      />
    </a-modal>

    <a-modal
      class="show-skill"
      :visible="showLanguage"
      @cancel="handleCancel"
      :closable="false"
      :maskClosable="false"
    >
      <template v-slot:title>
        <div class="skill-header">
          <p style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px">
            Programing Language
          </p>
          <div class="small-flex" style="display: flex">
            <a-button
              style="margin-left: 10px"
              class="btn-reset"
              @click="
                () => {
                  this.checkedPrograminglanguages = [];
                  this.notifyReset();
                }
              "
              >Reset</a-button
            >
            <a-input
              @change="(event) => (this.programinglanguageSearch = event.target.value)"
              style="max-width: 200px; margin-left: 5px"
              placeholder="Search programing language"
            />
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <a-button
          class="btn-cancel"
          @click="
            () => {
              handleCancel();
              this.checkedPrograminglanguages = this.searchPrograminglanguages;
            }
          "
          >Cancel</a-button
        >
        <a-button
          class="btn-confirm"
          @click="
            () => {
              handleCancel();
              this.searchPrograminglanguages = this.checkedPrograminglanguages;
              this.searchFrameworks = [];
              this.searchKnowledges = [];
              this.searchPlatforms = [];
              this.searchTools = [];
              this.checkedKnowledges = [];
              this.checkedPlatforms = [];
              this.checkedTools = [];
              this.checkedFrameworks = [];
              onClickSearch();
            }
          "
          >Confirm</a-button
        >
      </template>
      <a-checkbox-group
        :options="displayProgramingLanguage"
        :value="this.checkedPrograminglanguages"
        @change="onChangePrograminglanguages"
      />
    </a-modal>

    <a-modal
      class="show-skill"
      :visible="showFramework"
      @cancel="handleCancel"
      :closable="false"
      :maskClosable="false"
    >
      <template v-slot:title>
        <div class="skill-header">
          <p style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px">
            Framework
          </p>
          <div class="small-flex" style="display: flex">
            <a-button
              style="margin-left: 10px"
              class="btn-reset"
              @click="
                () => {
                  this.checkedFrameworks = [];
                  this.notifyReset();
                }
              "
              >Reset</a-button
            >
            <a-input
              @change="(event) => (this.frameworkSearch = event.target.value)"
              style="max-width: 200px; margin-left: 5px"
              placeholder="Search framework"
            />
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <a-button
          class="btn-cancel"
          @click="
            () => {
              handleCancel();
              this.checkedFrameworks = this.searchFrameworks;
            }
          "
          >Cancel</a-button
        >
        <a-button
          class="btn-confirm"
          @click="
            () => {
              handleCancel();
              this.searchFrameworks = this.checkedFrameworks;
              this.searchPrograminglanguages = [];
              this.searchKnowledges = [];
              this.searchPlatforms = [];
              this.searchTools = [];
              this.checkedKnowledges = [];
              this.checkedPlatforms = [];
              this.checkedTools = [];
              this.checkedPrograminglanguages = [];
              onClickSearch();
            }
          "
          >Confirm</a-button
        >
      </template>
      <a-checkbox-group
        :options="displayFramework"
        :value="this.checkedFrameworks"
        @change="onChangeFrameworks"
      />
    </a-modal>
  </div>
</template>

<script>
import axios from "axios";
import CourseDetail from "@/components/CourseDetail.vue";
import AllListPopularCourse from "@/components/AllListPopularCourse.vue";
import PopularTopics from "@/components/PopularTopics.vue";
import { FEConstants } from "../FEConstants";
import jwt_decode from "jwt-decode";
import ListFreeCourses from "@/components/ListFreeCourses.vue";

export default {
  name: "SearchByCareer",
  data() {
    return {
      numberList: 0,
      knowledges: [],
      platforms: [],
      tools: [],
      programinglanguages: [],
      frameworks: [],
      courses: [],
      careers: [],
      chosenCareer: "",
      lastCareer: "",
      detailCareer: [],
      loadingCourse: true,
      popularCoursesOfAll: [],
      loadingCardOfAll: true,
      titleList: [],
      dataCourseLists: [],
      loadingCourseSkill: true,
      topFreeCourses: [],
      freeCourseLoading: true,
      showKnowledge: false,
      showPlatform: false,
      showTool: false,
      showLanguage: false,
      showFramework: false,
      showCareer: false,
      knowledgeSearch: "",
      platformSearch: "",
      toolSearch: "",
      programinglanguageSearch: "",
      frameworkSearch: "",
      careerSearch: "",
      searchKnowledges: [],
      searchPlatforms: [],
      searchTools: [],
      searchPrograminglanguages: [],
      searchFrameworks: [],
      displayKnowledge: [],
      displayPlatfrom: [],
      displayTool: [],
      displayProgramingLanguage: [],
      displayFramework: [],
      webs: [],
      displayCourse: [],

      checkedKnowledges: [],
      checkedPlatforms: [],
      checkedTools: [],
      checkedPrograminglanguages: [],
      checkedFrameworks: [],
    };
  },
  components: {
    CourseDetail,
    AllListPopularCourse,
    PopularTopics,
    ListFreeCourses,
  },
  props: {
    skillName: String,
  },
  watch: {
    $route(to) {
      if (to.name === "SearchByCareer") {
        if (this.$route.query.career) {
          this.chosenCareer = this.$route.query.career;
          this.lastCareer = this.$route.query.career;
          this.getSkill(this.$route.query.career);
          this.onConfirmCareer();
        } else {
          this.getCourse();
        }
      }
    },
    toolSearch() {
      if (this.toolSearch != "") {
        this.displayTool = this.tools.filter((value) =>
          value.toLowerCase().startsWith(this.toolSearch.toLowerCase())
        );
      } else {
        this.displayTool = this.tools;
      }
    },
    knowledgeSearch() {
      if (this.knowledgeSearch != "") {
        this.displayKnowledge = this.knowledges.filter((value) =>
          value.toLowerCase().startsWith(this.knowledgeSearch.toLowerCase())
        );
      } else {
        this.displayKnowledge = this.knowledges;
      }
    },
    platformSearch() {
      if (this.platformSearch != "") {
        this.displayPlatfrom = this.platforms.filter((value) =>
          value.toLowerCase().startsWith(this.platformSearch.toLowerCase())
        );
      } else {
        this.displayPlatfrom = this.platforms;
      }
    },
    programinglanguageSearch() {
      if (this.programinglanguageSearch != "") {
        this.displayProgramingLanguage = this.programinglanguages.filter(
          (value) =>
            value
              .toLowerCase()
              .startsWith(this.programinglanguageSearch.toLowerCase())
        );
      } else {
        this.displayProgramingLanguage = this.programinglanguages;
      }
    },
    frameworkSearch() {
      if (this.frameworkSearch != "") {
        this.displayFramework = this.frameworks.filter((value) =>
          value.toLowerCase().startsWith(this.frameworkSearch.toLowerCase())
        );
      } else {
        this.displayFramework = this.frameworks;
      }
    },
  },
  methods: {
    selectWeb(value) {
      if (value != "All") {
        this.displayCourse = this.courses.filter((item) =>
          item.crsLink.includes(value.toLowerCase())
        );
      } else {
        this.displayCourse = this.courses;
      }
    },
    async getWeb() {
      await axios
        .get(`api/get_all_web/`)
        .then((res) => {
          res.data[0].value = res.data[0].value.replace("www.", "");
          this.webs = res.data.map((value) => {
            value.value = value.value.replace("www.", "");
            let result = value.value.slice(0, value.value.indexOf("."));
            return result.charAt(0).toUpperCase() + result.slice(1);
          });
          this.webs.splice(0, 0, "All");
          console.log(this.webs);
          this.freeCourseLoading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    selectAllKnowledge() {
      this.displayKnowledge.forEach((value) => {
        if (
          !this.checkedKnowledges.length ||
          this.checkedKnowledges.indexOf(value) < 0
        ) {
          this.checkedKnowledges.push(value);
        }
      });
    },
    selectAllPlatform() {
      this.displayPlatfrom.forEach((value) => {
        if (
          !this.checkedPlatforms.length ||
          this.checkedPlatforms.indexOf(value) < 0
        ) {
          this.checkedPlatforms.push(value);
        }
      });
    },
    selectAllTool() {
      this.displayTool.forEach((value) => {
        if (!this.checkedTools.length || this.checkedTools.indexOf(value) < 0) {
          this.checkedTools.push(value);
        }
      });
    },
    selectAllProgramLanguage() {
      this.displayProgramingLanguage.forEach((value) => {
        if (
          !this.checkedPrograminglanguages.length ||
          this.checkedPrograminglanguages.indexOf(value) < 0
        ) {
          this.checkedPrograminglanguages.push(value);
        }
      });
    },
    selectAllFramework() {
      this.displayFramework.forEach((value) => {
        if (
          !this.checkedFrameworks.length ||
          this.checkedFrameworks.indexOf(value) < 0
        ) {
          this.checkedFrameworks.push(value);
        }
      });
    },
    notifyReset() {
      this.$message.info({
        content: "All choices are removed!",
        key: "removechoice",
      });
    },
    handleCancel() {
      this.showCareer = false;
      this.showKnowledge = false;
      this.showPlatform = false;
      this.showTool = false;
      this.showLanguage = false;
      this.showFramework = false;
    },
    showModalCareer() {
      this.showCareer = true;
    },
    showModalKnowledge() {
      if (this.knowledges.length > 0) {
        this.showKnowledge = true;
      } else {
        this.$message.info({
          content: "There is no option available!",
          key: "notify",
        });
      }
    },
    showModalPlatfrom() {
      if (this.platforms.length > 0) {
        this.showPlatform = true;
      } else {
        this.$message.info({
          content: "There is no option available!",
          key: "notify",
        });
      }
    },
    showModalTool() {
      if (this.tools.length > 0) {
        this.showTool = true;
      } else {
        this.$message.info({
          content: "There is no option available!",
          key: "notify",
        });
      }
    },
    showModalLanguage() {
      if (this.programinglanguages.length > 0) {
        this.showLanguage = true;
      } else {
        this.$message.info({
          content: "There is no option available!",
          key: "notify",
        });
      }
    },
    showModalFramework() {
      if (this.frameworks.length > 0) {
        this.showFramework = true;
      } else {
        this.$message.info({
          content: "There is no option available!",
          key: "notify",
        });
      }
    },
    onClickReset() {
      this.checkedKnowledges = [];
      this.checkedPlatforms = [];
      this.checkedTools = [];
      this.checkedPrograminglanguages = [];
      this.checkedFrameworks = [];
      this.$message.info({
        content: "All choices are removed!",
        key: "removechoice",
      });
    },
    fetchCareer() {
      this.careers = JSON.parse(localStorage.getItem("career")).map(
        (e) => e.creTitle
      );
      this.detailCareer = JSON.parse(localStorage.getItem("career"));
    },
    storeCareerSearch(value) {
      let careerSearch = [];
      if (localStorage.getItem("recentCareer")) {
        careerSearch = JSON.parse(localStorage.getItem("recentCareer"));
      }
      careerSearch.splice(0, 0, value);
      careerSearch = careerSearch.slice(0, 30);
      localStorage.setItem("recentCareer", JSON.stringify(careerSearch));
    },
    getSkill(value) {
      let career = this.detailCareer.filter(
        (career) => career.creTitle === value
      );
      this.knowledges = career[0].knowledge.map((e) => e.value).sort();
      this.displayKnowledge = this.knowledges;
      this.platforms = career[0].platform.map((e) => e.value).sort();
      this.displayPlatfrom = this.platforms;
      this.tools = career[0].tool.map((e) => e.value).sort();
      this.programinglanguages = career[0].programinglanguage
        .map((e) => e.value)
        .sort();
      this.displayTool = this.tools;
      this.displayProgramingLanguage = this.programinglanguages;
      this.frameworks = career[0].framework.map((e) => e.value).sort();
      this.displayFramework = this.frameworks;
    },
    onChooseCareer(value) {
      this.chosenCareer = value.target.value;
    },
    onCancelCareer() {
      this.chosenCareer = this.lastCareer;
    },
    async onConfirmCareer() {
      this.lastCareer = this.chosenCareer;
      this.storeCareerSearch(this.chosenCareer);
      this.getSkill(this.chosenCareer);
      this.searchKnowledges = [];
      this.searchPlatforms = [];
      this.searchTools = [];
      this.searchPrograminglanguages = [];
      this.searchFrameworks = [];
      this.checkedKnowledges = [];
      this.checkedPlatforms = [];
      this.checkedTools = [];
      this.checkedPrograminglanguages = [];
      this.checkedFrameworks = [];
      let career = this.detailCareer.filter(
        (career) => career.creTitle === this.chosenCareer
      );
      this.loadingCourse = true;
      await axios({
        method: "GET",
        url: "api/get_course_from_career/",
        params: {
          id: career[0].id,
        },
      })
        .then((res) => {
          this.loadingCourse = false;
          this.courses = res.data;
          this.displayCourse = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async getCourse() {
      this.loadingCourse = true;
      await axios
        .get(`api/search_course/`)
        .then((res) => {
          this.loadingCourse = false;
          this.courses = res.data;
          this.displayCourse = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    onChangeKnowledge(checkedValues) {
      this.checkedKnowledges = checkedValues;
    },
    onChangePlatforms(checkedValues) {
      this.checkedPlatforms = checkedValues;
    },
    onChangeTools(checkedValues) {
      this.checkedTools = checkedValues;
    },
    onChangePrograminglanguages(checkedValues) {
      this.checkedPrograminglanguages = checkedValues;
    },
    onChangeFrameworks(checkedValues) {
      this.checkedFrameworks = checkedValues;
    },
    async onClickSearch() {
      this.loadingCourse = true;
      await axios
        .get(`api/filter_course_by_skill/`, {
          params: {
            knowledge: this.searchKnowledges,
            platform: this.searchPlatforms,
            tool: this.searchTools,
            programinglanguage: this.searchPrograminglanguages,
            framework: this.searchFrameworks,
          },
        })
        .then((res) => {
          if (res.data.length >= 5) {
            this.storeSkillSearch();
          }
          this.loadingCourse = false;
          this.courses = res.data;
          this.displayCourse = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    storeLocalStorage(key, baseArray) {
      let value = [];
      if (localStorage.getItem(key)) {
        value = JSON.parse(localStorage.getItem(key));
      }
      value = [].concat(baseArray, value);
      value = value.slice(0, 15);
      localStorage.setItem(key, JSON.stringify(value));
    },

    storeSkillSearch() {
      this.storeLocalStorage("recentKnowledge", this.checkedKnowledges);
      this.storeLocalStorage("recentPlatform", this.checkedPlatforms);
      this.storeLocalStorage("recentTool", this.checkedTools);
      this.storeLocalStorage(
        "recentPrograminglanguage",
        this.checkedPrograminglanguages
      );
      this.storeLocalStorage("recentFramework", this.checkedFrameworks);
    },
    getCountValueInArray(arr, type) {
      const counts = {};
      if (!arr) return counts;
      for (const value of arr) {
        if (value) {
          if (counts[value]) {
            counts[value].number += 1;
          } else {
            counts[value] = {
              number: 1,
              type: type,
            };
          }
        }
      }
      return counts;
    },
    createQueryListCard() {
      let knowledge = this.getCountValueInArray(
        JSON.parse(localStorage.getItem("recentKnowledge")),
        "knowledge"
      );
      let platform = this.getCountValueInArray(
        JSON.parse(localStorage.getItem("recentPlatform")),
        "platform"
      );
      let tool = this.getCountValueInArray(
        JSON.parse(localStorage.getItem("recentTool")),
        "tool"
      );
      let pograminglanguage = this.getCountValueInArray(
        JSON.parse(localStorage.getItem("recentPrograminglanguage")),
        "programinglanguage"
      );
      localStorage.removeItem("recentFramework");
      let framework = this.getCountValueInArray(
        JSON.parse(localStorage.getItem("recentFramework")),
        "framework"
      );
      let result = {
        ...knowledge,
        ...platform,
        ...tool,
        ...pograminglanguage,
        ...framework,
      };

      let sortedPopular = Object.keys(result).sort(function (a, b) {
        return -result[a].number + result[b].number;
      });
      let data = [];
      let type = [];
      for (let i = 0; i < FEConstants.NUMBER_LIST_CARD; i++) {
        if (!sortedPopular[i]) continue;
        data.push(sortedPopular[i]);
        type.push(result[sortedPopular[i]].type);
      }
      return { data: data, type: type };
    },
    async getPopularSkillCard(query) {
      this.loadingCourseSkill = true;
      let id = -1;
      if (localStorage.getItem("token")) {
        id = jwt_decode(localStorage.getItem("token")).user_id;
      }
      for (let i = 0; i < query.data.length; i++) {
        await axios
          .get(`api/popular_course_by_type/`, {
            params: {
              value: query.data[i],
              type: query.type[i],
              number: FEConstants.NUMBER_CARD_IN_LIST,
              uid: id,
            },
          })
          .then((res) => {
            if (res.data.length > 5) {
              this.dataCourseLists.push(res.data);
              this.titleList.push(query.data[i]);
              this.numberList += 1;
            }
            this.loadingCourseSkill = false;
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
    fetchSkill() {
      this.knowledges = JSON.parse(localStorage.getItem("knowledges"))
        .map((e) => e.value)
        .sort();
      this.displayKnowledge = this.knowledges;
      this.platforms = JSON.parse(localStorage.getItem("platforms"))
        .map((e) => e.value)
        .sort();
      this.displayPlatfrom = this.platforms;
      this.tools = JSON.parse(localStorage.getItem("tools"))
        .map((e) => e.value)
        .sort();
      this.displayTool = this.tools;
      this.programinglanguages = JSON.parse(
        localStorage.getItem("programinglanguages")
      )
        .map((e) => e.value)
        .sort();
      this.displayProgramingLanguage = this.programinglanguages;
      this.frameworks = JSON.parse(localStorage.getItem("frameworks"))
        .map((e) => e.value)
        .sort();
      this.displayFramework = this.frameworks;
    },
  },
  created() {
    document.title = "Explore Courses And Grow Your Career | Course Search";
    this.fetchCareer();
    this.getWeb();
    this.fetchSkill();
    if (this.$route.query.career) {
      this.chosenCareer = this.$route.query.career;
      this.lastCareer = this.$route.query.career;
      this.getSkill(this.$route.query.career);
      this.onConfirmCareer();
    } else {
      this.getCourse();
    }
  },
  computed: {
    isEmpty() {
      return this.lastCareer == "";
    },
    displayCareer() {
      if (this.careerSearch != "") {
        return this.careers.filter((value) =>
          value.toLowerCase().startsWith(this.careerSearch.toLowerCase())
        );
      } else {
        return this.careers;
      }
    },
    listSearch() {
      return [
        ...this.searchKnowledges,
        ...this.searchPlatforms,
        ...this.searchTools,
        ...this.searchPrograminglanguages,
        ...this.searchFrameworks,
      ].toString();
    },
  },
};
</script>

<style lang="scss">
.flex-display {
  display: flex !important;
  width: fit-content !important;
}

.search-screen {
  min-width: 200px;
  padding-left: 10px !important;
}
.filter-bar {
  border-color: rgb(223, 223, 223) !important;
  border-right-width: 2px !important;
  overflow-y: scroll;
  max-height: 600px !important;
}

.filter-bar::-webkit-scrollbar {
  width: 0 !important;
}
.justify-screen {
  justify-content: center !important;
  width: 100%;
}

.title-checklist {
  font-weight: 700;
  font-size: 1.3em !important;
}
.ant-checkbox-group-item,
.ant-radio-wrapper {
  display: block !important;
  margin-left: 1.5em !important;
  margin-bottom: 0.5em !important;
  font-size: 1em !important;
  font-weight: 500 !important;
}
.ant-checkbox-checked .ant-checkbox-inner {
  background-color: rgb(68, 211, 68) !important;
  border-color: rgb(68, 211, 68) !important;
  border-width: 2px !important;
}

.ant-radio-checked,
.ant-radio:hover {
  & .ant-radio-inner {
    border-color: rgb(68, 211, 68) !important;
    box-shadow: none !important;
    outline: none !important;
  }
}

.ant-radio,
.ant-radio-inner,
.ant-radio-checked::after,
.ant-radio:hover .ant-radio-inner {
  border-color: rgb(68, 211, 68) !important;
}

.ant-radio-inner::after {
  background-color: rgb(68, 211, 68) !important;
}
.ant-checkbox-inner,
.ant-checkbox-checked::after,
.ant-checkbox:hover .ant-checkbox-inner {
  border-color: rgb(68, 211, 68) !important;
  border-width: 2px !important;
}
.ant-checkbox,
.ant-checkbox-input {
  outline: none !important;
}

.ant-menu-submenu-title:hover {
  color: rgb(68, 211, 68) !important;
}

.ant-menu-submenu-arrow {
  &::after:hover {
    color: rgb(68, 211, 68) !important;
    border-color: rgb(68, 211, 68) !important;
  }
}
.ant-menu-submenu-title:hover span::after {
  color: rgb(68, 211, 68) !important;
}

@media all and (max-width: 600px) {
  .search-screen {
    padding-top: 10px !important;
    min-width: 200px;
    padding-left: 0px !important;
    justify-content: left !important;
    width: 100% !important;
  }
}
</style>

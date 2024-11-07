<template>
  <a-row type="flex" class="justify-screen popular-tabs">
    <a-col :xs="24" :lg="18">
      <span class="title-popular">Top paid courses</span>
      <a-select
        show-search
        placeholder="Select website"
        option-filter-prop="children"
        style="width: 200px; float: right !important; margin-top: 9px"
        class="web-select"
        :filter-option="filterOption"
        @change="selectWeb"
        default-value="All"
      >
        <a-select-option v-for="value in webs" :key="value" :value="value">
          {{ value }}
        </a-select-option>
      </a-select>
    </a-col>
    <a-col :xs="24" :lg="18">
      <ListCourseCard
        keyList="all"
        :courseDatas="popularCoursesOfAll"
        :loadingCard="loadingCardOfAll"
      ></ListCourseCard>
    </a-col>
    <a-col v-if="numberList > 0 && displayRecentView" :xs="24" :lg="18">
      <span class="title-popular">Recently viewed</span>
    </a-col>
    <a-col v-if="numberList > 0 && displayRecentView" :xs="24" :lg="18">
      <a-tabs :default-active-key="1">
        <a-tab-pane
          v-for="index in numberList"
          :key="index"
          :tab="titleList[index - 1]"
          force-render
        >
          <ListCourseCard
            :keyList="titleList[index - 1]"
            :courseDatas="dataCourseLists[index - 1]"
            :loadingCard="loadingCourseSkill"
          ></ListCourseCard>
        </a-tab-pane>
      </a-tabs>
    </a-col>
  </a-row>
</template>

<script>
import ListCourseCard from "@/components/ListCourseCard.vue";
import axios from "axios";
import { FEConstants } from "../FEConstants";
import jwt_decode from "jwt-decode";
export default {
  name: "AllListPopularCourse",
  components: {
    ListCourseCard,
  },
  props: {
    displayRecentView: Boolean,
  },
  data() {
    return {
      defaltTabtitle: "All",
      popularCoursesOfAll: [],
      loadingCardOfAll: true,
      numberList: 0,
      titleList: [],
      dataCourseLists: [],
      loadingCourseSkill: true,
      webs: [],
    };
  },
  created() {
    let queryPopular = this.createQueryListCard();
    this.getPopularSkillCard(queryPopular);
    this.getPopularCourse();
    this.getWeb();
  },
  methods: {
    async selectWeb(value) {
      this.loadingCardOfAll = true;
      let id = -1;
      if (localStorage.getItem("token")) {
        id = jwt_decode(localStorage.getItem("token")).user_id;
      }
      if (value != "All") {
        await axios
          .get(`api/popular_course_web/`, {
            params: {
              number: FEConstants.NUMBER_CARD_IN_LIST,
              uid: id,
              web: value,
            },
          })
          .then((res) => {
            if (res.data.length >= 5) {
              this.popularCoursesOfAll = res.data;
            } else {
              this.$message.info({
                content: "There is no course avalable now!",
                key: "find",
              });
            }
            this.loadingCardOfAll = false;
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        this.getPopularCourse();
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
          this.freeCourseLoading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async getPopularCourse() {
      this.loadingCardOfAll = true;
      let id = -1;
      if (localStorage.getItem("token")) {
        id = jwt_decode(localStorage.getItem("token")).user_id;
      }
      await axios
        .get(`api/popular_course/`, {
          params: {
            number: FEConstants.NUMBER_CARD_IN_LIST,
            uid: id,
          },
        })
        .then((res) => {
          this.popularCoursesOfAll = res.data;
          this.loadingCardOfAll = false;
        })
        .catch((err) => {
          console.log(err);
        });
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
  },
};
</script>

<style lang="scss">
.popular-tabs .ant-tabs-bar {
  margin-bottom: 0px !important;
  font-weight: 600;
  // margin-left: 3.5rem !important;
}
.popular-tabs .ant-tabs-tab-active,
.popular-tabs .ant-tabs-tab:hover {
  color: rgb(68, 211, 68) !important;
  // margin-left: 3.5rem !important;
}
.popular-tabs .ant-tabs-ink-bar {
  color: rgb(68, 211, 68) !important;
  background-color: rgb(68, 211, 68) !important;
}
.popular-tabs .ant-tabs-tab {
  text-transform: capitalize;
}
.title-popular {
  border-bottom: 2px solid rgb(68, 211, 68);
  font-size: 27px;
  font-weight: 700;
}
.web-select {
  margin-right: 4vw !important;
}
@media all and (max-width: 992px) {
  .web-select {
    margin-right: calc(4vw + 15px) !important;
  }
}
</style>

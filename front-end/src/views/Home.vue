<template>
  <div class="home">
    <div
      v-if="showBanner"
      class="banner"
      style="font-size: 16px; font-family: 'Myriad Pro'"
    >
      <strong>Welcome {{ username }}!</strong>
      <router-link to="/update-information" class="banner-text"
        >Complete your profile</router-link
      >
      <strong>to get better experience!</strong>
    </div>
    <img src="../assets/banner.png" />
    <a-button type="primary" class="button-start" @click="routerToSearch">
      EXPLORE COURSES RIGHT NOW!
    </a-button>
    <RecommendSpecificCourse/>
    <ListFreeCourses/>
    <AllListPopularCourse :displayRecentView="false"
    />
    <PopularTopics style="padding-bottom: 40px !important" />
  </div>
</template>

<script>
import axios from "axios";
import AllListPopularCourse from "@/components/AllListPopularCourse.vue";
import ListFreeCourses from "@/components/ListFreeCourses.vue";
import RecommendSpecificCourse from "@/components/RecommendSpecificCourse.vue";
import PopularTopics from "@/components/PopularTopics.vue";
import { FEConstants } from "../FEConstants";
import jwt_decode from "jwt-decode";
// @ is an alias to /src
export default {
  name: "HomePage",
  data() {
    return {
      detailCareer: [],
      loadingCourse: true,
      titleSpecificList: [],
      dataCourseSpecificLists: [],
      loadingCourseSpecificSkill: true,
      numberSpecificList: 0,
      showBanner: false,
      username: "",
    };
  },
  components: {
    AllListPopularCourse,
    PopularTopics,
    ListFreeCourses,
    RecommendSpecificCourse,
  },
  computed: {
    isBasicUser() {
      return (
        localStorage.getItem("token") &&
        jwt_decode(localStorage.getItem("token")).is_basicuser
      );
    },
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string
        .toLowerCase()
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
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
    routerToSearch() {
      this.$router.push({
        path: `/properties`,
      });
    },
    async getSpecificCourse() {
      this.topSpecificLoad = true;
      let id = -1;
      if (localStorage.getItem("token")) {
        id = jwt_decode(localStorage.getItem("token")).user_id;
      }
      if (id == -1) return;
      await axios({
        method: "GET",
        url: "api/user_information/",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        params: {
          id: jwt_decode(localStorage.getItem("token")).user_id,
        },
      })
        .then(async (res) => {
          let type = [];
          let value = [];
          let current_career = res.data.current_career[0]
            ? res.data.current_career[0].creTitle
            : null;
          let expected_career = res.data.hope_career[0]
            ? res.data.hope_career[0].creTitle
            : null;
          let knowledges = res.data.knowledge.map((value) => value.value);
          let platforms = res.data.platform.map((value) => value.value);
          let tool = res.data.tool.map((value) => value.value);
          let programinglanguage = res.data.programinglanguage.map(
            (value) => value.value
          );
          let framework = res.data.framework.map((value) => value.value);
          if (
            (knowledges.length == 0 &&
              platforms.length == 0 &&
              tool.length == 0 &&
              programinglanguage.length == 0 &&
              framework.length == 0) ||
            current_career == null ||
            expected_career == null
          ) {
            this.showBanner = true;
            this.username = res.data.name;
          }
          do {
            if (
              knowledges.length > 0 &&
              type.length < FEConstants.NUMBER_LIST_CARD
            ) {
              let val = Math.floor(Math.random() * knowledges.length);
              type.push("knowledge");
              value.push(knowledges[val]);
              knowledges = knowledges.filter(
                (item) => item !== knowledges[val]
              );
            }
          } while (
            Math.random < 0.75 &&
            type.length < FEConstants.NUMBER_LIST_CARD
          );

          do {
            if (
              platforms.length > 0 &&
              type.length < FEConstants.NUMBER_LIST_CARD
            ) {
              let val = Math.floor(Math.random() * platforms.length);
              type.push("platform");
              value.push(platforms[val]);
              platforms = platforms.filter((item) => item !== platforms[val]);
            }
          } while (
            Math.random < 0.75 &&
            type.length < FEConstants.NUMBER_LIST_CARD
          );

          do {
            if (tool.length > 0 && type.length < FEConstants.NUMBER_LIST_CARD) {
              let val = Math.floor(Math.random() * tool.length);
              type.push("tool");
              value.push(tool[val]);
              tool = tool.filter((item) => item !== tool[val]);
            }
          } while (
            Math.random < 0.75 &&
            type.length < FEConstants.NUMBER_LIST_CARD
          );

          do {
            if (
              programinglanguage.length > 0 &&
              type.length < FEConstants.NUMBER_LIST_CARD
            ) {
              let val = Math.floor(Math.random() * programinglanguage.length);
              type.push("programinglanguage");
              value.push(programinglanguage[val]);
              programinglanguage = programinglanguage.filter(
                (item) => item !== programinglanguage[val]
              );
            }
          } while (
            Math.random < 0.75 &&
            type.length < FEConstants.NUMBER_LIST_CARD
          );

          do {
            if (
              framework.length > 0 &&
              type.length < FEConstants.NUMBER_LIST_CARD
            ) {
              let val = Math.floor(Math.random() * framework.length);
              type.push("framework");
              value.push(framework[val]);
              framework = framework.filter((item) => item !== framework[val]);
            }
          } while (
            Math.random < 0.75 &&
            type.length < FEConstants.NUMBER_LIST_CARD
          );

          this.loadingCourseSpecificSkill = true;
          let id = -1;
          if (localStorage.getItem("token")) {
            id = jwt_decode(localStorage.getItem("token")).user_id;
          }
          for (let i = 0; i < type.length; i++) {
            await axios
              .get(`api/popular_course_by_type/`, {
                params: {
                  value: value[i],
                  type: type[i],
                  number: FEConstants.NUMBER_CARD_IN_LIST,
                  uid: id,
                },
              })
              .then((res) => {
                if (res.data.length > 5) {
                  this.dataCourseSpecificLists.push(res.data);
                  this.titleSpecificList.push(value[i]);
                  this.numberSpecificList += 1;
                }
                this.loadingCourseSpecificSkill = false;
              })
              .catch((err) => {
                console.log(err);
              });
          }
        })
        .catch((err) => console.log(err));
      await axios
        .get(`api/get_free_course/`, {
          params: {
            number: FEConstants.NUMBER_CARD_IN_LIST,
            uid: id,
          },
        })
        .then((res) => {
          this.topSpecificCourse = res.data;
          this.topSpecificLoad = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    document.title = "Course Search | Online Courses Exploring";
    this.getSpecificCourse();
    if (jwt_decode(localStorage.getItem("token")).is_dataadmin) {
      this.$router.push({
        path: `/dashboard`,
      });
    }
  },
};
</script>
<style scoped>
@font-face {
  font-family: "Myriad Pro";
  src: url("https://fonts.cdnfonts.com/s/492/MYRIADPRO-REGULAR.woff")
    format("woff");
}

.home img {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}
.home .button-start {
  background-color: rgb(0, 194, 0) !important;
  border-color: rgb(0, 194, 0) !important;
  border-radius: 0px !important;
  font-size: 1.8vw;
  float: right;
  margin-right: 5.8vw;
  top: -6.5vw !important;
  width: fit-content !important;
  height: fit-content !important;
  padding-right: 1vw !important;
  padding-left: 1vw !important;
  padding-top: 0.7vw !important;
  padding-bottom: 0.7vw !important;
  margin-bottom: -40px;
}
.button-start:hover {
  background-color: rgb(2, 146, 2) !important;
  border-color: rgb(2, 146, 2) !important;
}
.banner {
  position: relative;
  width: 100%;
  background-color: rgb(246, 250, 255) !important;
  padding: 10px;
}
.banner-text {
  color: rgb(0, 194, 0) !important;
  font-size: 16px !important;
  font-weight: 600;
  font-family: "Myriad Pro";
}
</style>

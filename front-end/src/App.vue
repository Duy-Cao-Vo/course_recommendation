<template>
  <div>
    <a-menu mode="horizontal" class="menu-bar">
      <a-menu-item key="mail"
        ><router-link to="/" id="brand-name"
          ><strong
            ><span style="position: relative; top: -6px !important"><span
              style="
                color: rgb(2, 202, 2) !important;
                font-size: 1.5rem !important;
              "
              >C</span
            >our</span
            ><span
              style="
                color: rgb(2, 202, 2) !important;
                font-size: 1.5rem !important;
              "
              >S</span
            >earch</strong
          ></router-link
        ></a-menu-item
      >
      <a-sub-menu v-if="!isDataAdmin" id="feature-selecting" class="menu-bar">
        <span slot="title" class="submenu-title-wrapper green-tex small-explore"
          ><strong>Explore</strong></span
        >
        <a-sub-menu key="setting:1" class="change-bg-color-hover-blue">
          <span slot="title"
            ><router-link to="/properties" class="feature-option"
              >Properties
            </router-link>
          </span>
          <a-sub-menu class="change-bg-color-hover-blue">
            <span slot="title" class="feature-option">Platform</span>
            <a-menu-item
              class="skill-value-item"
              v-for="item in platforms"
              :key="item"
              @click="clickPlatform"
              >{{ item }}</a-menu-item
            >
          </a-sub-menu>
          <a-sub-menu class="change-bg-color-hover-blue">
            <span slot="title" class="feature-option">Knowledge</span>
            <a-menu-item
              class="skill-value-item"
              v-for="item in knowledges"
              :key="item"
              @click="clickKnowledge"
              >{{ item }}</a-menu-item
            >
          </a-sub-menu>

          <a-sub-menu class="change-bg-color-hover-blue">
            <span slot="title" class="feature-option">Tool</span>
            <a-menu-item
              class="skill-value-item"
              v-for="item in tools"
              :key="item"
              @click="clickTool"
              >{{ item }}</a-menu-item
            >
          </a-sub-menu>
          <a-sub-menu class="change-bg-color-hover-blue">
            <span slot="title" class="feature-option">Language</span>
            <a-menu-item
              class="skill-value-item"
              v-for="item in programinglanguages"
              :key="item.id"
              @click="clickPrograminglanguages"
              >{{ item }}</a-menu-item
            >
          </a-sub-menu>
          <a-sub-menu class="change-bg-color-hover-blue">
            <span slot="title" class="feature-option">Framework</span>
            <a-menu-item
              class="skill-value-item"
              v-for="item in frameworks"
              :key="item"
              @click="clickFramework"
              >{{ item }}</a-menu-item
            >
          </a-sub-menu>
        </a-sub-menu>
        <a-sub-menu key="setting:3" class="change-bg-color-hover-blue">
          <span slot="title" style="color: black !important">Programs</span>
          <a-menu-item
            class="skill-value-item"
            v-for="item in careers"
            :key="item.id"
            @click="clickProgram"
            >{{ item.creTitle }}</a-menu-item
          >
        </a-sub-menu>
        <a-sub-menu key="setting:2" class="change-bg-color-hover-blue">
          <span slot="title"
            ><router-link to="/searchbycareer" class="feature-option"
              >Career</router-link
            ></span
          >
          <a-menu-item
            class="skill-value-item"
            v-for="item in careers"
            :key="item.creTitle"
            @click="clickCareer"
            >{{ item.creTitle }}</a-menu-item
          >
        </a-sub-menu>
      </a-sub-menu>
            <a-menu-item
        v-if="isDataAdmin"
        style="
          padding-left: 0px !important;
          margin-left: auto !important;
        "
      >
        <a-button
          type="primary"
          @click="onClickCrawl"
          class="log-in-btn log-in-small"
        >
          Import data
        </a-button>
      </a-menu-item>
      <a-menu-item v-if="!isDataAdmin">
        <form method="get" action="/properties">
          <a-input-search
            placeholder="Input course you want to search"
            class="search-bar hide-search-bar"
            name="query"
            @search="onSearch"
          />
        </form>
      </a-menu-item>
      <a-menu-item
        v-if="!token"
        style="
          padding-left: 0px !important;
          float: right;
          margin-left: auto !important;
        "
      >
        <a-button
          type="primary"
          @click="onClickLogIn"
          class="log-in-btn log-in-small"
        >
          Log In
        </a-button>
      </a-menu-item>
      <a-menu-item
        v-if="!token"
        style="padding-left: 0px; padding-right: 10px !important; float: right"
      >
        <a-button
          type="primary"
          class="sign-up-btn"
          @click="onClickSignUp"
          ghost
        >
          Sign Up
        </a-button>
      </a-menu-item>

      <a-sub-menu
        v-if="token"
        style="padding-right: 0px !important; float: right"
        class="user-space"
      >
        <span slot="title"
          ><a-icon
            type="user"
            style="transform: scale(2); margin-right: 0px"
            class="user-icon"
          />&nbsp;&nbsp;&nbsp;<strong class="username">{{
            username
          }}</strong></span
        >
        <a-menu-item
          v-if="isBasicUser"
          class="skill-value-item"
          @click="onClickProfile"
          >Your profile</a-menu-item
        >
        <a-menu-item
          v-if="isBasicUser"
          class="skill-value-item"
          @click="onClickManageLearning"
          >Your courses</a-menu-item
        >
        <a-menu-item class="skill-value-item" @click="onClickLogOut"
          >Log out</a-menu-item
        >
      </a-sub-menu>
      <a-menu-item
        v-if="isAccountAdmin"
        style="padding-right: 10px !important; float: right"
      >
        <a-button
          type="primary"
          @click="onClickAddUser"
          class="log-in-btn log-in-small"
        >
          Add user
        </a-button>
      </a-menu-item>
      <a-menu-item
        v-if="true"
        style="padding-right: 10px !important; float: right"
      >
      </a-menu-item>
    </a-menu>
    <router-view />
  </div>
</template>
<script>
import jwt_decode from "jwt-decode";
import axios from "axios";
export default {
  name: "SearchBySkill",
  data() {
    return {
      knowledges: [],
      platforms: [],
      tools: [],
      programinglanguages: [],
      frameworks: [],
      courses: [],
      careers: [],
      username: "",
    };
  },
  beforeCreate() {
    let now = new Date();
    if (Number(localStorage.getItem("token_date")) != now.getDate()) {
      localStorage.removeItem("token_date");
      localStorage.removeItem("token");
    }
    // if (!localStorage.getItem("knowledges")) {
    // }
  },
  async mounted() {
    await this.fetchSkill();
    await this.fetchCareer();
    this.getUsername();
    document.title = "Course Search | Online Courses Exploring";
  },
  computed: {
    token() {
      return localStorage.getItem("token");
    },
    isBasicUser() {
      return (
        localStorage.getItem("token") &&
        jwt_decode(localStorage.getItem("token")).is_basicuser
      );
    },
    isDataAdmin() {
      return (
        localStorage.getItem("token") &&
        jwt_decode(localStorage.getItem("token")).is_dataadmin
      );
    },
    isAccountAdmin() {
      return (
        localStorage.getItem("token") &&
        jwt_decode(localStorage.getItem("token")).is_accountadmin
      );
    },
  },
  methods: {
    onSearch(value) {
      this.$router.push({
        path: `/properties`,
        query: {
          query: value,
        },
      });
    },
    async getUsername() {
      await axios({
        method: "GET",
        url: "api/get_username/",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        params: {
          id: jwt_decode(localStorage.getItem("token")).user_id,
        },
      })
        .then((res) => {
          this.username = res.data.name;
        })
        .catch((err) => console.log(err));
    },
    onClickProfile() {
      this.$router.push({
        path: `/user-profile`,
      });
    },
    onClickLogOut() {
      localStorage.removeItem("token");
      this.$router.go(this.$router.currentRoute);
    },
    async fetchCareer() {
      let knowledges = JSON.parse(localStorage.getItem("knowledges")).map(
        (e) => e.value
      );
      let platforms = JSON.parse(localStorage.getItem("platforms")).map(
        (e) => e.value
      );
      let tools = JSON.parse(localStorage.getItem("tools")).map((e) => e.value);
      let programinglanguages = JSON.parse(
        localStorage.getItem("programinglanguages")
      ).map((e) => e.value);
      let frameworks = JSON.parse(localStorage.getItem("frameworks")).map(
        (e) => e.value
      );
      await axios
        .get(`api/get_career/`)
        .then((res) => {
          res.data.forEach((value) => {
            value.knowledge = value.knowledge.filter(
              (skill) => knowledges.indexOf(skill.value) >= 0
            );
            value.platform = value.platform.filter(
              (skill) => platforms.indexOf(skill.value) >= 0
            );
            value.tool = value.tool.filter(
              (skill) => tools.indexOf(skill.value) >= 0
            );
            value.programinglanguage = value.programinglanguage.filter(
              (skill) => programinglanguages.indexOf(skill.value) >= 0
            );
            value.framework = value.framework.filter(
              (skill) => frameworks.indexOf(skill.value) >= 0
            );
          });
          localStorage.setItem("career", JSON.stringify(res.data));
          this.careers = JSON.parse(localStorage.getItem("career"));
        })
        .catch((err) => {
          console.log(err);
        });
    },
    async fetchSkill() {
      await axios
        .get(`api/get_skill/`)
        .then((res) => {
          localStorage.setItem(
            "knowledges",
            JSON.stringify(res.data.knowledges)
          );
          localStorage.setItem("platforms", JSON.stringify(res.data.platforms));
          localStorage.setItem("tools", JSON.stringify(res.data.tools));
          localStorage.setItem(
            "programinglanguages",
            JSON.stringify(res.data.programinglanguages)
          );
          localStorage.setItem(
            "frameworks",
            JSON.stringify(res.data.frameworks)
          );
          this.knowledges = JSON.parse(localStorage.getItem("knowledges"))
            .slice(0, 10)
            .map((e) => e.value);
          this.platforms = JSON.parse(localStorage.getItem("platforms"))
            .slice(0, 10)
            .map((e) => e.value);
          this.tools = JSON.parse(localStorage.getItem("tools"))
            .slice(0, 10)
            .map((e) => e.value);
          this.programinglanguages = JSON.parse(
            localStorage.getItem("programinglanguages")
          )
            .slice(0, 10)
            .map((e) => e.value);
          this.frameworks = JSON.parse(localStorage.getItem("frameworks"))
            .slice(0, 10)
            .map((e) => e.value);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    clickProgram(value) {
      this.$router.push({
        path: `/programs`,
        query: { career: value.key },
      });
    },
    clickCareer(value) {
      console.log(value)
      this.$router.push({
        path: `/searchbycareer`,
        query: { career: value.key },
      });
    },
    clickPlatform(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.key, type: "platform" },
      });
    },
    onClickManageLearning() {
      this.$router.push({
        path: `/managelearning`,
      });
    },
    clickKnowledge(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.key, type: "knowledge" },
      });
    },
    clickTool(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.key, type: "tool" },
      });
    },
    clickPrograminglanguages(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.key, type: "programinglanguage" },
      });
    },
    onClickSignUp() {
      this.$router.push({
        path: `/sign-up`,
      });
    },
    onClickLogIn() {
      this.$router.push({
        path: `/login`,
      });
    },
    onClickCrawl() {
      this.$router.push({
        path: `/crawl`,
      });
    },
    onClickAddUser() {
      this.$router.push({
        path: `/add-user`,
      });
    },
    clickFramework(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.key, type: "framework" },
      });
    },
  },
};
</script>

<style lang="scss">
.username {
  color: black !important;
}
.user-space:hover .username {
  color: rgb(2, 202, 2) !important;
}
.user-icon {
  color: rgb(2, 202, 2) !important;
}
.sign-up-btn {
  border-color: rgb(2, 202, 2) !important;
  color: rgb(2, 202, 2) !important;
  font-weight: 600 !important;
}

.log-in-btn {
  background-color: rgb(2, 202, 2) !important;
  border-color: rgb(2, 202, 2) !important;
  font-weight: 600 !important;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.ant-input {
  &:focus,
  &:hover {
    border-color: rgb(2, 202, 2) !important;
    outline: none !important;

    box-shadow: none !important;
  }
}

ul .change-bg-color-hover-blue:hover {
  background-color: rgb(240, 255, 254) !important;
}
.change-bg-color-hover-blue li:hover {
  background-color: rgb(240, 255, 254) !important;
}
#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.ant-click-animating-node {
  position: static !important;
}

.skill-value-item {
  color: black !important;
  margin-top: 0px !important;
  margin-bottom: 0px !important;
}
.skill-value-item {
  text-transform: capitalize;
}
.skill-value-item:hover {
  color: rgb(2, 202, 2) !important;
  font-weight: 600 !important;
  background: green !important;
}
.menu-bar {
  background-color: rgb(236, 236, 236) !important;
}

.ant-menu-item:hover .feature-option,
.ant-menu-submenu-title:hover .feature-option {
  color: rgb(2, 202, 2) !important;
  font-weight: 600 !important;
}
.ant-menu-item:hover #brand-name {
  color: rgb(2, 202, 2) !important;
}
.ant-menu-item #brand-name {
  font-size: 1.3rem !important;
}
.green-tex {
  color: rgb(2, 202, 2) !important;
  font-size: 1.2rem;
}
.ant-menu-submenu-arrow:hover {
  color: rgb(2, 202, 2) !important;
  background-color: rgb(2, 202, 2) !important;
}
.ant-menu-sub .ant-menu-item {
  background-color: white !important;
}
.ant-menu-sub .ant-menu-item {
  font-weight: 450;
}

.ant-menu-item-selected #brand-name,
.ant-menu-item-selected .feature-option,
.ant-menu-item .feature-option,
.ant-menu-item #brand-name,
.ant-menu-submenu-selected,
.ant-menu-submenu-title .feature-option {
  color: black !important;
}

.ant-menu-item #brand-name {
  font-size: 1.025rem;
}
#brand-name:hover {
  text-decoration: none !important;
}
.ant-menu-submenu,
.ant-menu-submenu-selected,
.ant-menu-item-selected,
.ant-menu-item {
  border-color: transparent !important;
}

.ant-menu-submenu:hover {
  color: rgb(2, 202, 2) !important;
  border-color: rgb(2, 202, 2) !important;
}

.search-bar {
  width: 300px !important;
}
.search-bar .ant-input {
  height: 40px !important;
  font-size: 1.05rem;
  color: black !important;
}

@media all and (max-width: 800px) {
  .hide-search-bar {
    display: none !important;
  }
}

@media all and (max-width: 600px) {
  .course-detail .ant-card-body {
    width: 55%;
  }
  .button-add,
  .button-detail {
    font-size: 13px !important;
    padding: 0px 10px !important;
    position: relative !important;
  }
  .course-detail .ant-card-actions {
    margin-left: auto !important;
    margin-right: auto !important;
  }
  .sign-up-btn {
    display: none !important;
  }
}
.user-space .user-icon {
  position: relative;
  top: -3px;
}
@media all and (max-width: 500px) {
  #brand-name {
    transform: scale(0.9);
  }
  .small-explore {
    font-size: 15px !important;
  }
  .sign-up-btn {
    display: none !important;
  }
  .menu-bar .ant-menu-item {
    padding-left: 5px;
    padding-right: 5px;
  }
  .log-in-small {
    font-size: 12px !important;
    padding: 7px 7px !important;
  }
}
</style>

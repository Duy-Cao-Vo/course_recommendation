<template>
  <a-row type="flex" class="user-tabs" justify="center">
    <a-col :xs="24" :lg="18">
      <h2 style="text-align: center !important">Your profile</h2>
    </a-col>
    <a-col :xs="24" :lg="18">
      <a-button class="button-edit" @click="onClickEdit"
        ><a-icon type="edit" />Edit profile</a-button
      >
    </a-col>
    <a-col :xs="24" :lg="18">
      <a-tabs :default-active-key="1" tab-position="left">
        <a-tab-pane :key="1" tab="Basic Information">
          <a-input
            size="large"
            addon-before="Username"
            class="username-show"
            :key="username"
            :default-value="username"
            disabled
            style="margin-bottom: 10px"
          />

          <a-input
            size="large"
            addon-before="Level"
            class="username-show"
            :key="level"
            :default-value="level"
            disabled
            style="margin-bottom: 10px"
          />

          <a-input
            size="large"
            addon-before="Current career"
            class="username-show"
            :key="current_career"
            :default-value="current_career"
            disabled
            style="margin-bottom: 10px"
          />

          <a-input
            size="large"
            addon-before="Expected career"
            class="username-show"
            :key="expected_career"
            :default-value="expected_career"
            disabled
            style="margin-bottom: 10px"
          />
        </a-tab-pane>
        <a-tab-pane :key="2" tab="Concerned Skills">
          <div v-if="knowledges.length != 0">
            <h4>Knowledge</h4>
            <a-button
              v-for="skill in knowledges"
              :key="skill"
              size="default"
              :value="skill"
              class="skill-button-user"
              @click="clickKnowledge"
            >
              {{ skill }}
            </a-button>
          </div>
          <div v-if="tools.length != 0">
            <h4>Tool</h4>
            <a-button
              v-for="skill in tools"
              :key="skill"
              :value="skill"
              size="default"
              class="skill-button-user"
              @click="clickTool"
            >
              {{ skill }}
            </a-button>
          </div>
          <div v-if="frameworks.length != 0">
            <h4>Framework</h4>
            <a-button
              v-for="skill in frameworks"
              :key="skill"
              :value="skill"
              size="default"
              class="skill-button-user"
              @click="clickFramework"
            >
              {{ skill }}
            </a-button>
          </div>
          <div v-if="platforms.length != 0">
            <h4>Platform</h4>
            <a-button
              v-for="skill in platforms"
              :key="skill"
              :value="skill"
              size="default"
              class="skill-button-user"
              @click="clickPlatform"
            >
              {{ skill }}
            </a-button>
          </div>
          <div v-if="programinglanguages.length != 0">
            <h4>Programinglanguage</h4>
            <a-button
              v-for="skill in programinglanguages"
              :key="skill"
              :value="skill"
              size="default"
              class="skill-button-user"
              @click="clickPrograminglanguages"
            >
              {{ skill }}
            </a-button>
          </div>
        </a-tab-pane>
      </a-tabs>
    </a-col>
  </a-row>
</template>

<script>
import jwt_decode from "jwt-decode";
import axios from "axios";
export default {
  name: "UserProfile",
  data() {
    return {
      username: "",
      current_career: "",
      expected_career: "",
      level: "",
      knowledges: [],
      platforms: [],
      tools: [],
      programinglanguages: [],
      frameworks: [],
    };
  },
  created() {
    if (!localStorage.getItem("token")) {
      this.$router.push({
        path: `/`,
      });
    } else {
      this.fetchUserInformation();
    }
  },
  methods: {
    clickPlatform(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "platform" },
      });
    },
    clickKnowledge(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "knowledge" },
      });
    },
    clickTool(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "tool" },
      });
    },
    clickPrograminglanguages(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "programinglanguage" },
      });
    },
    clickFramework(value) {
      this.$router.push({
        path: `/properties`,
        query: { value: value.target.value, type: "framework" },
      });
    },
    onClickEdit() {
      this.$router.push({
        path: `/update-information`,
      });
    },
    async fetchUserInformation() {
      await axios({
        method: "GET",
        url: "api/user_information/",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        params: {
          id: jwt_decode(localStorage.getItem("token")).user_id,
        },
      })
        .then((res) => {
          this.username = res.data.name;
          this.current_career = res.data.current_career[0]
            ? res.data.current_career[0].creTitle
            : null;
          this.expected_career = res.data.hope_career[0]
            ? res.data.hope_career[0].creTitle
            : null;
          this.knowledges = res.data.knowledge.map((value) => value.value);
          this.platforms = res.data.platform.map((value) => value.value);
          this.tools = res.data.tool.map((value) => value.value);
          this.programinglanguages = res.data.programinglanguage.map(
            (value) => value.value
          );
          this.frameworks = res.data.framework.map((value) => value.value);
          this.level = res.data.level[0] ? res.data.level[0].value : null;
        })
        .catch((err) => console.log(err));
    },
  },
};
</script>

<style lang="scss">
.button-edit {
  font-size: 1.2em !important;
  font-weight: 500 !important;
  background-color: rgb(68, 211, 68) !important;
  border-color: rgb(68, 211, 68) !important;
  display: block !important;
  margin-left: auto !important;
  margin-top: 10px !important;
  margin-bottom: 10px !important;
  color: white !important;
}
.username-show .ant-input {
  background-color: white !important;
  color: black !important;
}
.username-show .ant-input-group-addon {
  font-size: 16px !important;
}
.user-tabs .ant-tabs-bar {
  margin-bottom: 0px !important;
  font-weight: 600;
  background-color: rgb(245, 245, 245);
  // margin-left: 3.5rem !important;
}
.user-tabs .ant-tabs-tab-active,
.user-tabs .ant-tabs-tab:hover {
  color: rgb(68, 211, 68) !important;
  // margin-left: 3.5rem !important;
}
.user-tabs .ant-tabs-ink-bar {
  color: rgb(68, 211, 68) !important;
  background-color: rgb(68, 211, 68) !important;
}
.user-tabs .ant-tabs-tab {
  text-transform: capitalize;
  text-align: left !important;
  // font-size: ;
}
.button-edit .anticon-edit {
  position: relative;
  top: -4px;
}
.skill-button-user {
  background-color: transparent !important;
  border-color: rgb(216, 216, 216) !important;
  color: rgb(2, 202, 2) !important;
  font-weight: 600 !important;
  margin: 5px !important;
  border-radius: 100px !important;
  border-width: 2px !important;
  text-transform: capitalize !important;
}
.skill-button-user:hover {
  border-color: rgb(2, 202, 2) !important;
  color: rgb(2, 202, 2) !important;
}
</style>
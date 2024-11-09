<template>
  <div class="update-profile">
    <a-steps
      :current="current"
      @change="onChange"
      class="step-update"
      style="margin-bottom: 50px !important; margin-top: 20px; padding: 0 70px"
    >
      <a-step
        title="Basic information"
        description="Complete all your basic information"
      />
      <a-step title="Skills" description="Choose kills you concern" />
      <a-step
        title="Expect career"
        description="The career you want to focus on"
      />
    </a-steps>
    <div v-if="current == 0" class="setting-basic-infor">
      <a-input
        size="large"
        class="update-username"
        addon-before="Username"
        :value="localUsername"
        key="username"
        @change="updateUsername"
        style="margin-bottom: 10px !important; font-size: 17px !important"
      />
      <label class="level-area">
        <span
          style="
            padding-left: 11px;
            padding-right: 11px;
            display: inline-block;
            width: 150px;
          "
        >
          <strong style="font-size: 17px !important">Current career:</strong>
        </span>
        <a-select
          size="large"
          :value="localChosenCurrentCareer"
          style="width: 200px !important; margin-bottom: 10px !important"
          key="current_career"
          @change="onChooseCurrentCareer"
        >
          <a-select-option :value="null">None</a-select-option>
          <a-select-option
            v-for="career in careers"
            :value="career"
            :key="career"
          >
            {{ career }}
          </a-select-option>
        </a-select>
      </label>
      <label class="level-area">
        <span
          style="
            padding-left: 11px;
            padding-right: 11px;
            display: inline-block;
            width: 150px;
          "
        >
          <strong style="font-size: 17px !important">Level:</strong>
        </span>
        <a-select
          key="level"
          :value="localChosenLevel"
          size="large"
          @change="onChooseLevel"
        >
          <a-select-option value="Beginner"> Beginner </a-select-option>
          <a-select-option value="Intermediate"> Intermediate </a-select-option>
          <a-select-option value="Advanced"> Advanced </a-select-option>
        </a-select>
      </label>

      <div>
        <a-button
          size="large"
          type="primary"
          class="btn-next"
          v-if="current != 2"
          @click="moveNextStep"
          >Next</a-button
        >
      </div>
    </div>
    <div v-if="current == 1" class="setting-skill">
      <a-row :gutter="[8, 16]" type="flex" justify="center">
        <a-col :lg="4" :md="10" :xs="24">
          <a-menu
            class="skill-choice"
            style="width: 100%"
            :default-selected-keys="['1']"
            mode="inline"
          >
            <a-menu-item
              class="btn-title-skill"
              key="Knowledges"
              @click="showModalKnowledge"
            >
              Knowledge
            </a-menu-item>
          </a-menu>
        </a-col>
        <a-col :lg="4" :md="10" :xs="24">
          <a-menu
            class="skill-choice"
            style="width: 100%"
            :default-selected-keys="['1']"
            mode="inline"
          >
            <a-menu-item
              class="btn-title-skill"
              key="platfrom"
              @click="showModalPlatfrom"
            >
              Platform
            </a-menu-item>
          </a-menu>
        </a-col>
        <a-col :lg="4" :md="10" :xs="24">
          <a-menu
            class="skill-choice"
            style="width: 100%"
            :default-selected-keys="['1']"
            mode="inline"
          >
            <a-menu-item
              class="btn-title-skill"
              key="tool"
              @click="showModalTool"
            >
              Tool
            </a-menu-item>
          </a-menu>
        </a-col>
        <a-col :lg="4" :md="10" :xs="24">
          <a-menu
            class="skill-choice"
            style="width: 100%"
            :default-selected-keys="['1']"
            mode="inline"
          >
            <a-menu-item
              class="btn-title-skill"
              key="language"
              @click="showModalLanguage"
            >
              Program Language
            </a-menu-item>
          </a-menu>
        </a-col>
        <a-col :lg="4" :md="10" :xs="24">
          <a-menu
            class="skill-choice"
            style="width: 100%"
            :default-selected-keys="['1']"
            mode="inline"
          >
            <a-menu-item
              class="btn-title-skill"
              key="framework"
              @click="showModalFramework"
            >
              Framework
            </a-menu-item>
          </a-menu>
        </a-col>
      </a-row>
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
            <p
              style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px"
            >
              Knowledge
            </p>
            <div style="display: flex">
              <a-button
                style="margin-left: 10px"
                class="btn-reset"
                @click="
                  () => {
                    this.localCheckedKnowledges = [];
                    this.notifyReset();
                  }
                "
                >Reset</a-button
              >
              <a-input
                @change="(event) => (this.knowledgeSearch = event.target.value)"
                style="max-width: 200px; margin-left: 5px"
                placeholder="Search skill"
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
                this.localCheckedKnowledges = this.searchKnowledges;
              }
            "
            >Cancel</a-button
          >
          <a-button
            class="btn-confirm"
            @click="
              () => {
                handleCancel();
                this.searchKnowledges = this.localCheckedKnowledges;
              }
            "
            >Confirm</a-button
          >
        </template>
        <a-checkbox-group
          :options="displayKnowledge"
          :value="this.localCheckedKnowledges"
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
            <p
              style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px"
            >
              Platform
            </p>
            <div style="display: flex">
              <a-button
                style="margin-left: 10px"
                class="btn-reset"
                @click="
                  () => {
                    this.localCheckedPlatforms = [];
                    this.notifyReset();
                  }
                "
                >Reset</a-button
              >
              <a-input
                @change="(event) => (this.platformSearch = event.target.value)"
                style="max-width: 200px; margin-left: 5px"
                placeholder="Search skill"
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
                this.localCheckedPlatforms = this.searchPlatforms;
              }
            "
            >Cancel</a-button
          >
          <a-button
            class="btn-confirm"
            @click="
              () => {
                handleCancel();
                this.searchPlatforms = this.localCheckedPlatforms;
              }
            "
            >Confirm</a-button
          >
        </template>
        <a-checkbox-group
          :options="displayPlatfrom"
          :value="this.localCheckedPlatforms"
          @change="onChangePlatforms"
        />
      </a-modal>

      <a-modal
        class="show-skill"
        :visible="showTool"
        :closable="false"
        :maskClosable="false"
      >
        <template v-slot:footer>
          <a-button
            class="btn-cancel"
            @click="
              () => {
                handleCancel();
                this.localCheckedTools = this.searchTools;
              }
            "
            >Cancel</a-button
          >
          <a-button
            class="btn-confirm"
            @click="
              () => {
                handleCancel();
                this.searchTools = this.localCheckedTools;
              }
            "
            >Confirm</a-button
          >
        </template>
        <template v-slot:title>
          <div class="skill-header">
            <p
              style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px"
            >
              Tool
            </p>
            <div style="display: flex">
              <a-button
                style="margin-left: 10px"
                class="btn-reset"
                @click="
                  () => {
                    this.localCheckedTools = [];
                    this.notifyReset();
                  }
                "
                >Reset</a-button
              >
              <a-input
                @change="(event) => (this.toolSearch = event.target.value)"
                style="max-width: 200px; margin-left: 5px"
                placeholder="Search skill"
              />
            </div>
          </div>
        </template>
        <a-checkbox-group
          :options="displayTool"
          :value="this.localCheckedTools"
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
            <p
              style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px"
            >
              Programing Language
            </p>
            <div style="display: flex">
              <a-button
                style="margin-left: 10px"
                class="btn-reset"
                @click="
                  () => {
                    this.localCheckedPrograminglanguages = [];
                    this.notifyReset();
                  }
                "
                >Reset</a-button
              >
              <a-input
                @change="
                  (event) =>
                    (this.programinglanguageSearch = event.target.value)
                "
                style="max-width: 200px; margin-left: 5px"
                placeholder="Search skill"
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
                this.localCheckedPrograminglanguages =
                  this.searchPrograminglanguages;
              }
            "
            >Cancel</a-button
          >
          <a-button
            class="btn-confirm"
            @click="
              () => {
                handleCancel();
                this.searchPrograminglanguages =
                  this.localCheckedPrograminglanguages;
              }
            "
            >Confirm</a-button
          >
        </template>
        <a-checkbox-group
          :options="displayProgramingLanguage"
          :value="this.localCheckedPrograminglanguages"
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
            <p
              style="margin-bottom: 0px; padding-top: 4px; padding-bottom: 4px"
            >
              Framework
            </p>
            <div style="display: flex">
              <a-button
                style="margin-left: 10px"
                class="btn-reset"
                @click="
                  () => {
                    this.localCheckedFrameworks = [];
                    this.notifyReset();
                  }
                "
                >Reset</a-button
              >
              <a-input
                @change="(event) => (this.frameworkSearch = event.target.value)"
                style="max-width: 200px; margin-left: 5px"
                placeholder="Search skill"
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
                this.localCheckedFrameworks = this.searchFrameworks;
              }
            "
            >Cancel</a-button
          >
          <a-button
            class="btn-confirm"
            @click="
              () => {
                handleCancel();
                this.searchFrameworks = this.localCheckedFrameworks;
              }
            "
            >Confirm</a-button
          >
        </template>

        <a-checkbox-group
          :options="displayFramework"
          :value="this.localCheckedFrameworks"
          @change="onChangeFrameworks"
        />
      </a-modal>
      <div>
        <a-button
          size="large"
          type="primary"
          class="btn-next"
          v-if="current != 2"
          @click="moveNextStep"
          >Next</a-button
        >
      </div>
    </div>
    <div v-if="current == 2" class="setting-basic-infor">
      <label class="level-area">
        <span
          style="
            padding-left: 11px;
            padding-right: 11px;
            display: inline-block;
            width: 150px;
          "
        >
          <strong style="font-size: 17px !important">Expected career:</strong>
        </span>
        <a-select
          :value="localChosenHopeCareer"
          size="large"
          style="width: 200px !important"
          key="hope-career"
          @change="onChooseHopeCareer"
        >
          <a-select-option
            v-for="career in careers"
            :value="career"
            :key="career"
          >
            {{ career }}
          </a-select-option>
        </a-select>
      </label>
      <div>
        <a-button
          size="large"
          type="primary"
          class="btn-finish"
          v-if="current == 2"
          @click="onClickFinish"
          >Finish</a-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "UpdateInformation",
  data() {
    return {
      current: 0,
      careers: [],
      knowledges: [],
      platforms: [],
      tools: [],
      programinglanguages: [],
      frameworks: [],
      showKnowledge: false,
      showPlatform: false,
      showTool: false,
      showLanguage: false,
      showFramework: false,
      knowledgeSearch: "",
      platformSearch: "",
      toolSearch: "",
      programinglanguageSearch: "",
      frameworkSearch: "",
      searchKnowledges: [],
      searchPlatforms: [],
      searchTools: [],
      searchPrograminglanguages: [],
      searchFrameworks: [],
      localUsername: this.username,
      localChosenCurrentCareer: this.chosenCurrentCareer,
      localChosenHopeCareer: this.chosenHopeCareer,
      localCheckedKnowledges: this.checkedKnowledges,
      localCheckedPlatforms: this.checkedPlatforms,
      localCheckedTools: this.checkedTools,
      localCheckedPrograminglanguages: this.checkedPrograminglanguages,
      localCheckedFrameworks: this.checkedFrameworks,
      localChosenLevel: this.chosenLevel,
    };
  },
  props: {
    username: String,
    checkedKnowledges: Array,
    checkedPlatforms: Array,
    checkedTools: Array,
    checkedPrograminglanguages: Array,
    checkedFrameworks: Array,
    chosenHopeCareer: String,
    chosenCurrentCareer: String,
    chosenLevel: String,
  },
  created() {
    if (!localStorage.getItem("token")) {
      this.$router.push({
        path: `/`,
      });
    } else {
      this.fetchSkill();
      this.fetchCareer();
      this.fetchUserInformation();
    }
  },
  methods: {
    notifyReset() {
      this.$message.info({
        content: "All choices are removed!",
        key: "removechoice",
      });
    },
    handleCancel() {
      this.showKnowledge = false;
      this.showPlatform = false;
      this.showTool = false;
      this.showLanguage = false;
      this.showFramework = false;
    },
    showModalKnowledge() {
      this.showKnowledge = true;
    },
    showModalPlatfrom() {
      this.showPlatform = true;
    },
    showModalTool() {
      this.showTool = true;
    },
    showModalLanguage() {
      this.showLanguage = true;
    },
    showModalFramework() {
      this.showFramework = true;
    },
    onChange(current) {
      this.current = current;
    },
    updateUsername(value) {
      this.localUsername = value.target.value;
    },
    async onClickFinish() {
      this.$message.loading({ content: "Updating...", key: "updating" });
      await axios({
        method: "POST",
        url: "api/update_profile/",
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        data: {
          id: jwt_decode(localStorage.getItem("token")).user_id,
          username: this.username ? this.username : null,
          level: this.chosenLevel ? this.chosenLevel : null,
          hopecareer: this.chosenHopeCareer ? this.chosenHopeCareer : null,
          currentcareer: this.chosenCurrentCareer
            ? this.chosenCurrentCareer
            : null,
          knowledge: this.searchKnowledges ? this.searchKnowledges : [],
          platform: this.searchPlatforms ? this.searchPlatforms : [],
          tool: this.searchTools ? this.searchTools : [],
          programinglanguage: this.searchPrograminglanguages
            ? this.searchPrograminglanguages
            : [],
          framework: this.searchFrameworks ? this.searchFrameworks : [],
        },
      })
        .then(() => {
          this.$message.success({
            content: "Update success!",
            key: "updating",
          });
          this.$router.push({
            path: `/`,
          });
          this.$router.go(this.$router.currentRoute);
        })
        .catch((err) => {
          console.log(err);
          this.$message.info({ content: "Update fail!", key: "updating" });
        });
    },
    moveNextStep() {
      this.current += 1;
    },
    fetchCareer() {
      this.careers = JSON.parse(localStorage.getItem("career")).map(
        (e) => e.creTitle
      );
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
          this.localUsername = res.data.name;
          this.localChosenCurrentCareer = res.data.current_career[0]
            ? res.data.current_career[0].creTitle
            : null;
          this.localChosenHopeCareer = res.data.hope_career[0]
            ? res.data.hope_career[0].creTitle
            : null;
          this.localCheckedKnowledges = res.data.knowledge.map(
            (value) => value.value
          );
          this.localCheckedPlatforms = res.data.platform.map((value) => value.value);
          this.localCheckedTools = res.data.tool.map((value) => value.value);
          this.localCheckedPrograminglanguages = res.data.programinglanguage.map(
            (value) => value.value
          );
          this.localCheckedFrameworks = res.data.framework.map(
            (value) => value.value
          );
          this.localChosenLevel = res.data.level[0] ? res.data.level[0].value : null;

          this.searchKnowledges = res.data.knowledge.map(
            (value) => value.value
          );
          this.searchPlatforms = res.data.platform.map((value) => value.value);
          this.searchTools = res.data.tool.map((value) => value.value);
          this.searchPrograminglanguages = res.data.programinglanguage.map(
            (value) => value.value
          );
          this.searchFrameworks = res.data.framework.map(
            (value) => value.value
          );

          this.$forceUpdate();
        })
        .catch((err) => console.log(err));
    },
  onChooseLevel(value) {
      this.localChosenLevel = value;
    },
    onChooseHopeCareer(value) {
      this.localChosenHopeCareer = value;
    },
    onChooseCurrentCareer(value) {
      this.localChosenCurrentCareer = value;
    },
    onChangeKnowledge(checkedValues) {
      this.localCheckedKnowledges = checkedValues;
    },
    onChangePlatforms(checkedValues) {
      this.localCheckedPlatforms = checkedValues;
    },
    onChangeTools(checkedValues) {
      this.localCheckedTools = checkedValues;
    },
    onChangePrograminglanguages(checkedValues) {
      this.localCheckedPrograminglanguages = checkedValues;
    },
    onChangeFrameworks(checkedValues) {
      this.localCheckedFrameworks = checkedValues;
    },
    fetchSkill() {
      this.knowledges = JSON.parse(localStorage.getItem("knowledges"))
        .map((e) => e.value)
        .sort();
      this.platforms = JSON.parse(localStorage.getItem("platforms"))
        .map((e) => e.value)
        .sort();
      this.tools = JSON.parse(localStorage.getItem("tools"))
        .map((e) => e.value)
        .sort();
      this.programinglanguages = JSON.parse(
        localStorage.getItem("programinglanguages")
      )
        .map((e) => e.value)
        .sort();
      this.frameworks = JSON.parse(localStorage.getItem("frameworks"))
        .map((e) => e.value)
        .sort();
    },
  },
  computed: {
    displayTool() {
      if (this.toolSearch != "") {
        return this.tools.filter((value) =>
          value.toLowerCase().includes(this.toolSearch.toLowerCase())
        );
      } else {
        return this.tools;
      }
    },
    displayKnowledge() {
      if (this.knowledgeSearch != "") {
        return this.knowledges.filter((value) =>
          value.toLowerCase().includes(this.knowledgeSearch.toLowerCase())
        );
      } else {
        return this.knowledges;
      }
    },
    displayPlatfrom() {
      if (this.platformSearch != "") {
        return this.platforms.filter((value) =>
          value.toLowerCase().includes(this.platformSearch.toLowerCase())
        );
      } else {
        return this.platforms;
      }
    },
    displayProgramingLanguage() {
      if (this.programinglanguageSearch != "") {
        return this.programinglanguages.filter((value) =>
          value
            .toLowerCase()
            .includes(this.programinglanguageSearch.toLowerCase())
        );
      } else {
        return this.programinglanguages;
      }
    },
    displayFramework() {
      if (this.frameworkSearch != "") {
        return this.frameworks.filter((value) =>
          value.toLowerCase().includes(this.frameworkSearch.toLowerCase())
        );
      } else {
        return this.frameworks;
      }
    },
  },
};
</script>

<style lang="scss">
.update-profile .skill-choice {
  padding-right: 1px;
  border-radius: 5px;
  border: 2px solid rgb(68, 211, 68);
}

.update-profile .btn-title-skill::after {
  display: none !important;
}

.step-update .ant-steps-item-container:hover {
  .ant-steps-item-title,
  .ant-steps-item-description,
  .ant-steps-item-icon,
  .ant-steps-icon {
    border-color: rgb(2, 202, 2) !important;
    color: rgb(2, 202, 2) !important;
  }
}
.step-update .ant-steps-item-icon {
  border-color: rgb(2, 202, 2) !important;
  background-color: transparent !important;
  .ant-steps-icon {
    color: rgb(2, 202, 2) !important;
  }
}
.step-update .ant-steps-item-finish {
  .ant-steps-item-icon,
  .ant-steps-icon {
    border-color: rgb(2, 202, 2) !important;
    color: rgb(2, 202, 2) !important;
    background: transparent !important;
  }
  .ant-steps-item-tail::after {
    border-color: rgb(2, 202, 2) !important;
    color: rgb(2, 202, 2) !important;
    background-color: rgb(2, 202, 2) !important;
  }
}

.update-username .ant-input-group-addon {
  font-size: 17px !important;
}
.btn-finish {
  border-radius: 0px !important;
  width: 100%;
  margin-top: 20px;
  font-size: 20px !important;
  font-weight: 600 !important;
  background-color: rgb(2, 202, 2) !important;
}
.btn-next {
  border-radius: 0px !important;
  margin-top: 20px;
  display: block !important;
  margin: 20px auto !important;
  // margin-right: auto !important;
  font-size: 20px !important;
  font-weight: 600 !important;
  background-color: rgb(2, 202, 2) !important;
}

.setting-basic-infor {
  margin-left: auto !important;
  margin-right: auto !important;
  width: 400px !important;
}
.update-username .ant-input-group-addon {
  background-color: transparent !important;
  border-color: transparent !important;
}
.update-username .ant-input {
  border-radius: 0px !important;
}
.level-area .ant-select-selection {
  width: 120px;
}
.update-profile i {
  position: relative;
  top: -3px;
}

.ant-select:hover .ant-select-selection,
.ant-select:focus .ant-select-selection {
  border-color: rgb(2, 202, 2) !important;
  outline: none !important;
  box-shadow: none !important;
}

.skill-choice .ant-menu {
  overflow-y: scroll;
  max-height: 600px !important;
}
.skill-choice .ant-menu::-webkit-scrollbar {
  width: 0 !important;
}
</style>
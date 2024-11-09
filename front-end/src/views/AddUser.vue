<template>
  <div class="signup-space">
    <a-card
      title="Create user"
      :bordered="false"
      style="width: 400px"
    >
      <a-input
        class="email-input"
        type="email"
        placeholder="Username"
        @change="inputUsername"
        @keyup.enter="onClickCreate"
      >
        <template v-slot:addonBefore>
          <a-icon type="user" style="transform: scale(1.25)" />
        </template>
      </a-input>
      <a-input
        class="email-input"
        type="email"
        placeholder="Email"
        @change="inputEmail"
        @keyup.enter="onClickCreate"
      >
        <template v-slot:addonBefore>
          <a-icon type="mail" style="transform: scale(1.25)" />
        </template>
      </a-input>
      <a-input
        class="email-input"
        placeholder="Enter password"
        type="password"
        @change="inputPassword"
        @keyup.enter="onClickCreate"
      >
        <template v-slot:addonBefore>
          <a-icon type="lock" style="transform: scale(1.25)" />
        </template>
      </a-input>
      <a-input
        class="email-input"
        placeholder="Confirm password"
        type="password"
        @change="retypePassword"
        @keyup.enter="onClickCreate"
      >
        <template v-slot:addonBefore>
          <a-icon type="lock" style="transform: scale(1.25)" />
        </template>
      </a-input>
      <label class="level-area">
        <span
          style="
            padding-right: 11px;
            display: inline-block;
            width: 150px;
          "
        >
          <strong style="font-size: 15px !important">Type user:</strong>
        </span>
        <a-select key="level" :value="localType" size="large" @change="onChooseType">
          <a-select-option value="dataadmin"> Data Admin </a-select-option>
          <a-select-option value="accountadmin">
            Account Admin
          </a-select-option>
        </a-select>
      </label>
      <a-button
        type="primary"
        class="log-in-btn"
        style="
          width: 100%;
          font-size: 16px;
          border-radius: 0px;
          margin-top: 15px;
          margin-bottom: 15px;
        "
        @click="onClickCreate"
      >
        Create account
      </a-button>
    </a-card>
  </div>
</template>

<script>
import axios from "axios";
import jwt_decode from "jwt-decode";
export default {
  name: "AddUser",
  props: {
    username: String,
    email: String,
    password: String,
    rePassword: String,
    type: String,
  },
  data() {
    return {
      localUsername: this.username,
      localEmail: this.email,
      localPassword: this.password,
      localRePassword: this.rePassword,
      localType: this.type,
    };
  },
  mounted() {
    if (!localStorage.getItem("token") || !jwt_decode(localStorage.getItem("token")).is_accountadmin) {
      this.$router.push({
        path: `/`,
      });
    }
  },
  methods: {
    onChooseType(value) {
      this.localType = value;
      console.log(this.localType)
    },
    inputUsername(value) {
      this.localUsername = value.target.value;
    },
    inputEmail(value) {
      this.localEmail = value.target.value;
    },
    inputPassword(value) {
      this.localPassword = value.target.value;
    },
    retypePassword(value) {
      this.localRePassword = value.target.value;
    },
    async onClickCreate() {
      if (
        this.localUsername != "" &&
        this.localEmail != "" &&
        this.localPassword != "" &&
        this.localPassword == this.localRePassword
        && this.localType && this.localType != ""
      ) {
        let api = "register_account_admin/";
        if(this.localType == "dataadmin") {
          api = "register_data_admin/"
        }

        this.$message.loading({ content: "Waiting...", key: "signup" });
        await axios({
          method: "POST",
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          url: "api/" + api,
          data: {
            username: this.localUsername,
            email: this.localEmail,
            password: this.localPassword,
          },
        })
          .then(() => {
            this.$message.success({
              content: "Account is created!",
              key: "signup",
            });
          })
          .catch(() =>
            this.$message.info({
              content: "Please use another email address!",
              key: "signup",
            })
          );
      } else {
        this.$message.info({
          content: "Please check your information!",
          key: "signup",
        });
      }
    },
  },
};
</script>

<style>
.email-input .ant-input-group-addon {
  width: 0px !important;
}
.signup-space .ant-card-head-title {
  font-size: 20px;
}
.signup-space .ant-card {
  margin-left: auto;
  margin-right: auto;
  border: 1px solid green;
  padding: 0px 5px 20px 5px;
  margin-top: 50px;
}
.signup-space .email-input {
  padding-bottom: 15px;
  /* padding-bottom: 5px; */
}
</style>
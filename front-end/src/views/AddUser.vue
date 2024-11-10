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
        <a-icon slot="addonBefore" type="user" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        type="email"
        placeholder="Email"
        @change="inputEmail"
        @keyup.enter="onClickCreate"
      >
        <a-icon slot="addonBefore" type="mail" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        placeholder="Enter password"
        type="password"
        @change="inputPassword"
        @keyup.enter="onClickCreate"
      >
        <a-icon slot="addonBefore" type="lock" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        placeholder="Confirm password"
        type="password"
        @change="retypePassword"
        @keyup.enter="onClickCreate"
      >
        <a-icon slot="addonBefore" type="lock" style="transform: scale(1.25)" />
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
        <a-select key="level" :value="type" size="large" @change="onChooseType">
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
  mounted() {
    if (!localStorage.getItem("token") || !jwt_decode(localStorage.getItem("token")).is_accountadmin) {
      this.$router.push({
        path: `/`,
      });
    }
  },
  methods: {
    onChooseType(value) {
      this.type = value;
      console.log(this.type)
    },
    inputUsername(value) {
      this.username = value.target.value;
    },
    inputEmail(value) {
      this.email = value.target.value;
    },
    inputPassword(value) {
      this.password = value.target.value;
    },
    retypePassword(value) {
      this.rePassword = value.target.value;
    },
    async onClickCreate() {
      if (
        this.username != "" &&
        this.email != "" &&
        this.password != "" &&
        this.password == this.rePassword
        && this.type && this.type != "" 
      ) {
        let api = "register_account_admin/";
        if(this.type == "dataadmin") {
          api = "register_data_admin/"
        }

        this.$message.loading({ content: "Waiting...", key: "signup" });
        await axios({
          method: "POST",
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          url: "api/" + api,
          data: {
            username: this.username,
            email: this.email,
            password: this.password,
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
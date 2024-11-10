<template>
  <div class="signup-space">
    <a-card
      title="Sign up and start learning"
      :bordered="false"
      style="width: 400px"
    >
      <a-input
        class="email-input"
        type="email"
        placeholder="Username"
        @change="inputUsername"
        @keyup.enter="onClickRegister"
      >
        <a-icon slot="addonBefore" type="user" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        type="email"
        placeholder="Email"
        @change="inputEmail"
        @keyup.enter="onClickRegister"
      >
        <a-icon slot="addonBefore" type="mail" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        placeholder="Enter password"
        type="password"
        @change="inputPassword"
        @keyup.enter="onClickRegister"
      >
        <a-icon slot="addonBefore" type="lock" style="transform: scale(1.25)" />
      </a-input>
      <a-input
        class="email-input"
        placeholder="Confirm password"
        type="password"
        @change="retypePassword"
        @keyup.enter="onClickRegister"
      >
        <a-icon slot="addonBefore" type="lock" style="transform: scale(1.25)" />
      </a-input>
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
        @click="onClickRegister"
      >
        Sign up
      </a-button>
      <p>
        Already have an account?<a
          href="/login"
          style="font-weight: 600; color: green !important"
        >
          Log in</a
        >
      </p>
    </a-card>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignUp",
  props: {
    username: String,
    email: String,
    password: String,
    rePassword: String,
  },
  mounted() {
    if (localStorage.getItem("token")) {
      this.$router.push({
        path: `/`,
      });
    }
  },
  methods: {
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
    async onClickRegister() {
      if (
        this.username != "" &&
        this.email != "" &&
        this.password != "" &&
        this.password == this.rePassword
      ) {
        this.$message.loading({ content: 'Waiting...', key: "signup" });
        await axios({
          method: "POST",
          url: "api/register/",
          data: {
            username: this.username,
            email: this.email,
            password: this.password,
          },
        })
          .then(() => {
            this.$router.push({
              path: `/login`,
            });
            this.$message.success({ content: 'Account is created!', key: "signup" });
          })
          .catch(() => this.$message.info({ content: 'Please use another email address!', key: "signup" }));
      } else {
        this.$message.info({ content: 'Please check your information!', key: "signup" });
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
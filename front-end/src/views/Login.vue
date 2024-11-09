<template>
  <div class="login">
    <a-input
      class="email-input"
      type="email"
      placeholder="Email"
      @change="inputEmail"
      @keyup.enter="onClickLogin"
    >
      <template v-slot:addonBefore>
        <a-icon type="mail" style="transform: scale(1.25)" />
      </template>
    </a-input>
    <a-input
      class="password-input"
      type="password"
      placeholder="Password"
      @change="inputPassword"
      @keyup.enter="onClickLogin"
    >
      <template v-slot:addonBefore>
        <a-icon type="lock" style="transform: scale(1.25)" />
      </template>
    </a-input>
    <a-button
      type="primary"
      class="login-btn"
      @click="onClickLogin"
    >
      Login
    </a-button>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  props: {
    email: String,
    password: String,
  },
  data() {
    return {
      localEmail: this.email,
      localPassword: this.password,
    };
  },
  methods: {
    inputEmail(event) {
      this.localEmail = event.target.value;
    },
    inputPassword(event) {
      this.localPassword = event.target.value;
    },
    onClickLogin() {
      // Handle login logic here
    },
  },
};
</script>

<style>
.email-input .ant-input-group-addon {
  width: 0px !important;
}
.login-space .ant-card-head-title {
  font-size: 20px;
}
.login-space .ant-card {
  margin-left: auto;
  margin-right: auto;
  border: 1px solid green;
  padding: 0px 5px 20px 5px;
  margin-top: 50px;
}
.login-space .email-input {
  padding-bottom: 15px;
  /* padding-bottom: 5px; */
}
.signup-space i, .login-space i {
  position: relative;
  top: -3px !important;
}
</style>
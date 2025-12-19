/* eslint-env node */
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/vue3-recommended",
    "@vue/eslint-config-typescript",
    "@vue/eslint-config-prettier",
  ],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    extraFileExtensions: [".vue"],
    tsconfigRootDir: __dirname,
  },
  overrides: [
    {
      files: ["src/**/*.{ts,tsx,vue}"],
      parserOptions: {
        project: ["./tsconfig.json"],
      },
    },
  ],
  ignorePatterns: ["dist/**", "node_modules/**"],
  rules: {
    "no-console": "warn",
    "no-debugger": "warn",
    "vue/multi-word-component-names": "off",
    "@typescript-eslint/no-explicit-any": "off",
  },
};

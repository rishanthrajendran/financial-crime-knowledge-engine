// ESLint Flat Config for Next.js 16.x
// @see https://nextjs.org/docs/basic-features/eslint#eslint-config

import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import nextPlugin from "@next/eslint-plugin-next";

export default [
  // Recommended base configs
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  
  {
    plugins: {
      "@next/next": nextPlugin,
    },
    rules: {
      // Next.js specific rules
      "@next/next/no-html-link-for-pages": "error",
    },
    files: ["**/*.{js,jsx,ts,tsx}"],
  },
  
  {
    ignores: [".next/**", "node_modules/**", "next-env.d.ts"],
  },
];

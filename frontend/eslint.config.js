import js from '@eslint/js'
import ts from 'typescript-eslint'
import vue from 'eslint-plugin-vue'
import prettier from 'eslint-config-prettier'
import tailwind from 'eslint-plugin-tailwindcss'
import globals from 'globals'

export default [
  {
    ignores: ['.nuxt/**', 'node_modules/**', 'dist/**', '.output/**'],
  },
  js.configs.recommended,
  ...ts.configs.recommended,
  ...vue.configs['flat/recommended'],
  ...tailwind.configs['flat/recommended'],
  prettier,
  {
    files: ['**/*.{js,ts,vue}'],
    languageOptions: {
      parserOptions: {
        parser: ts.parser,
      },
      globals: {
        ...globals.browser,
        ...globals.node,
        // Nuxt 3 auto-imports
        ref: 'readonly',
        computed: 'readonly',
        onMounted: 'readonly',
        useRuntimeConfig: 'readonly',
        useFetch: 'readonly',
        defineProps: 'readonly',
        defineEmits: 'readonly',
        definePageMeta: 'readonly',
        watch: 'readonly',
        reactive: 'readonly',
        toRef: 'readonly',
        toRefs: 'readonly',
        nextTick: 'readonly',
      },
    },
    rules: {
      'vue/multi-word-component-names': 'off',
      '@typescript-eslint/no-unused-vars': 'warn',
      'tailwindcss/no-custom-classname': 'off',
      'tailwindcss/classnames-order': 'warn',
    },
  },
]

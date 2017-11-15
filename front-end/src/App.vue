<template>
  <v-app>
    
    <v-navigation-drawer temporary v-model="sidebar">
      <v-list>
        <v-list-tile
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          :color="item.color">
          <v-list-tile-content>{{ item.title }}</v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar fixed flat color="white">
      <span class="hidden-sm-and-up">
        <v-toolbar-side-icon @click.stop="sidebar = !sidebar">
        </v-toolbar-side-icon>
      </span>
      <v-toolbar-title>
        <router-link to="/" tag="span" style="cursor: pointer">
          <v-icon large>
            business
          </v-icon>
          <!-- {{ appTitle }} -->
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn
          flat
          v-for="item in menuItems"
          :key="item.title"
          :color="item.color"
          :to="item.path">
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    
    <main style="background-color:white;">
      <v-container pa-0 fluid>
        <router-view></router-view>
      </v-container>
    </main>
    
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
        appTitle: 'HSK',
        sidebar: false,
        menuItems: [
          { title: 'Career', path: '/career', icon: 'home', color: "grey"},
          { title: 'Company', path: '/company', icon: 'face', color: "grey" },
          { title: 'Pricing', path: '/pricing', icon: 'face', color: "grey"},
          { title: 'Login', path: '/signin', icon: 'face', color: "blue"},
          { title: 'Sign Up', path: '/signup', icon: 'lock_open', color: "green"}
        ]
      }
    }
  }
</script>

<style lang="stylus">
  @import './stylus/main'

  @require '../../node_modules/vuetify/src/stylus/settings/_colors'
 
  $theme := {
    primary: $red.darken-2
    accent: $red.accent-2
    secondary: $grey.lighten-1
    info: $blue.lighten-1
    warning: $amber.darken-2
    error: $red.accent-4
    success: $green.lighten-2
  }
</style>
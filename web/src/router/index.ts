import {createRouter, createWebHashHistory} from "vue-router";
// import {userMainStore} from "@/store";

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/login"
    },
    {
      path: "/login",
      component: () => import("@/views/login/LoginView.vue"),
      name: "login"
    },
    {
      path: "/panel",
      component: () => import("@/views/panel/MainPanelView.vue"),
      redirect: "/panel/",
      children: [
        {
          path: "/panel/",
          component: () => import("@/views/panel/child/PanelIndex.vue"),
          name: "panelIndex"
        },
        {
          path: "/panel/assessment",
          component: () => import("@/views/panel/child/PanelAssessmentView.vue"),
          name: "panelAssessment"
        },
        {
          path: "/panel/me",
          component: () => import("@/views/panel/child/PanelMe.vue"),
          name: "panelMe"
        },
        {
          path: "/panel/manage",
          component: () => import("@/views/panel/child/PanelManageView.vue"),
          name: "panelManage"
        },
        {
          path: "/panel/comprehensive",
          component: () => import("@/views/panel/child/PanelComprehensiveView.vue"),
          name: "panelComprehensive"
        }
      ]
    }
  ],
});

// router.beforeEach((to, from, next) => {
//     if (to.path === "/login") {
//         return next();
//     }
//     const user = window.sessionStorage.getItem("user")
//     const userType = window.localStorage.getItem("auth")
//     if (!user) {
//         return next("/login");
//     }
//     if (to.meta.auth) {
//         return userType === "admin" ? next() : next(from.path)
//     }
//     // also see https://pinia.vuejs.org/zh/core-concepts/outside-component-usage.html for more detail
//     const store = userMainStore()
//     if (!store.user.name) {
//         store.updateUserByRequest(userType).then(() => next())
//     } else {
//         next();
//     }
// });

export default router;

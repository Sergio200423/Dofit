"use strict";

document.addEventListener('DOMContentLoaded', function () {
  'use strict';
  console.log("Chart.js disponible:", typeof Chart !== 'undefined');
  feather.replace();

  // Sidebar persistente
  var sidebar = document.querySelector('.sidebar');
  var sidebarBtns = document.querySelectorAll('.sidebar-toggle');
  if (sidebar) {
    var sidebarState = localStorage.getItem('sidebarState');
    if (sidebarState === 'collapsed') {
      sidebar.classList.add('hidden');
      sidebarBtns.forEach(function(btn) { btn.classList.add('rotated'); });
    } else {
      sidebar.classList.remove('hidden');
      sidebarBtns.forEach(function(btn) { btn.classList.remove('rotated'); });
    }
  }

  // Sidebar toggle
  if (sidebar && sidebarBtns.length) {
    sidebarBtns.forEach(function(sidebarBtn) {
      sidebarBtn.addEventListener('click', function () {
        sidebarBtns.forEach(function(btn) { btn.classList.toggle('rotated'); });
        sidebar.classList.toggle('hidden');
        if (sidebar.classList.contains('hidden')) {
          localStorage.setItem('sidebarState', 'collapsed');
        } else {
          localStorage.setItem('sidebarState', 'expanded');
        }
      });
    });
  }

  // Dropdowns de usuario y notificaciones
  var userDdBtnList = document.querySelectorAll('.dropdown-btn');
  var userDdList = document.querySelectorAll('.users-item-dropdown');
  var layer = document.querySelector('.layer');
  if (userDdList.length && userDdBtnList.length && layer) {
    userDdBtnList.forEach(function(userDdBtn) {
      userDdBtn.addEventListener('click', function (e) {
        layer.classList.add('active');
        userDdList.forEach(function(userDd) {
          if (e.currentTarget.nextElementSibling == userDd) {
            userDd.classList.toggle('active');
          } else {
            userDd.classList.remove('active');
          }
        });
      });
    });
    layer.addEventListener('click', function () {
      userDdList.forEach(function(userDd) {
        userDd.classList.remove('active');
      });
      layer.classList.remove('active');
    });
  }

  // Dark mode
  var darkMode = localStorage.getItem('darkMode');
  var darkModeToggle = document.querySelector('.theme-switcher');
  var enableDarkMode = function () {
    document.body.classList.add('darkmode');
    localStorage.setItem('darkMode', 'enabled');
  };
  var disableDarkMode = function () {
    document.body.classList.remove('darkmode');
    localStorage.setItem('darkMode', null);
  };
  if (darkMode === 'enabled') {
    enableDarkMode();
  }
  if (darkModeToggle) {
    darkModeToggle.addEventListener('click', function () {
      darkMode = localStorage.getItem('darkMode');
      if (darkMode !== 'enabled') {
        enableDarkMode();
      } else {
        disableDarkMode();
      }
    });
  }
});
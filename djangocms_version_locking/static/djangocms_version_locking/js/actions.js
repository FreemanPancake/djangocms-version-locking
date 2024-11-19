"use strict";

(function ($) {
  if (!$) {
    return;
  }

  $(function () {
    var createBurgerMenu = function createBurgerMenu(row) {
      /* create burger menu anchor section */
      var anchor = document.createElement('A');
      var cssclass = document.createAttribute('class');
      cssclass.value = 'btn cms-action-btn closed cms-action-burger';
      anchor.setAttributeNode(cssclass);
      //  create burger menu title
      var title = document.createAttribute('title');
      title.value = 'Actions';
      anchor.setAttributeNode(title);
      // create burger menu icon
      var menu_icon = document.createElement('span');
      menu_icon.className = "cms-icon cms-icon-menu";
      anchor.appendChild(menu_icon);

      /* create options container */
      var optionsContainer = document.createElement('DIV');
      cssclass = document.createAttribute('class');
      cssclass.value = 'cms-pagetree-dropdown-menu ' + // main selector for the menu
      'cms-pagetree-dropdown-menu-arrow-right-top'; // keeps the menu arrow in position

      optionsContainer.setAttributeNode(cssclass);
      var ul = document.createElement('UL');
      cssclass = document.createAttribute('class');
      cssclass.value = 'cms-pagetree-dropdown-menu-inner';
      ul.setAttributeNode(cssclass);
      /* get the existing actions and move them into the options container */

      var li;
      var text;
      var actions = $(row).children('.field-list_actions');

      if (!actions.length) {
        /* skip any rows without actions to avoid errors */
        return;
      }

      var actions_btn = $(actions[0]).children('.cms-action-btn');
      if (actions_btn.length <=3) {
        return;
      } else {
        actions_btn.each(function (index, item) {
          /* exclude preview/view and edit buttons */
          if (item.classList.contains('cms-action-preview') ||
              item.classList.contains('cms-action-view') ||
              item.classList.contains('cms-action-edit')) {
            return;
          }
  
          li = document.createElement('LI');
          /* create an anchor from the item */
  
          var li_anchor = document.createElement('A');
          cssclass = document.createAttribute('class');
          cssclass.value = 'cms-action-burger-options-anchor';
  
          if ($(item).hasClass('cms-form-get-method')) {
            /* ensure the fake-form selector is propagated to the new anchor */
            cssclass.value += ' cms-form-get-method';
          }
  
          li_anchor.setAttributeNode(cssclass);
          var href = document.createAttribute('href');
          href.value = $(item).attr('href');
          li_anchor.setAttributeNode(href);
          /* move the an image element */
  
          var existing_icon_span = $(item).children('span');
          li_anchor.appendChild(existing_icon_span[0]);
          /* create the button text */
  
          text = document.createTextNode(item.title);
          var span = document.createElement('SPAN');
          span.appendChild(text); // construct the button
  
          li.appendChild(li_anchor);
          li_anchor.appendChild(span);
          ul.appendChild(li);
          /* destroy original replaced buttons */
  
          actions[0].removeChild(item);
        });
      }
      
      /* add the options to the drop-down */
      optionsContainer.appendChild(ul);
      $(actions[0]).children('.cms-action-btn:last').after(anchor);
      document.body.appendChild(optionsContainer);
      /* listen for burger menu clicks */

      anchor.addEventListener('click', function (ev) {
        ev.stopPropagation();
        toggleBurgerMenu(anchor, optionsContainer);
      });
      /* close burger menu if clicking outside */

      $(window).click(function () {
        closeBurgerMenu();
      });
    };

    var toggleBurgerMenu = function toggleBurgerMenu(burgerMenuAnchor, optionsContainer) {
      var bm = $(burgerMenuAnchor);
      var op = $(optionsContainer);
      var closed = bm.hasClass('closed');
      closeBurgerMenu();

      if (closed) {
        bm.removeClass('closed');
        bm.addClass('open');
        op.removeClass('closed');
        op.addClass('open');
      } else {
        bm.addClass('closed');
        bm.removeClass('open');
        op.addClass('closed');
        op.removeClass('open');
      }

      var pos = bm.offset();
      op.css('left', pos.left - 200);
      op.css('top', pos.top);
    };

    var closeBurgerMenu = function closeBurgerMenu() {
      $('.cms-pagetree-dropdown-menu').removeClass('open');
      $('.cms-pagetree-dropdown-menu').addClass('closed');
      $('.cms-action-btn').removeClass('open');
      $('.cms-action-btn').addClass('closed');
    };

    $('#result_list').find('tr').each(function (index, item) {
      createBurgerMenu(item);
    });
    /* it is not possible to put a form inside a form, so
      actions have to create their own form on click */

    var fakeForm = function fakeForm(e) {
      var action = $(e.currentTarget);
      var formMethod = action.attr('class').indexOf('cms-form-get-method') !== -1 ? 'GET' : 'POST';
      if (formMethod == 'GET') return
      e.preventDefault();

      var csrfToken = '<input type="hidden" name="csrfmiddlewaretoken" value="' + document.cookie.match(/csrftoken=([^;]*);?/)[1] + '">';
      var fakeForm = $('<form style="display: none" action="' + action.attr('href') + '" method="' + formMethod + '">' + csrfToken + '</form>');
      var keepSideFrame = action.attr('class').indexOf('js-keep-sideframe') !== -1; // always break out of the sideframe, cause it was never meant to open cms views inside it

      try {
        if (!keepSideFrame) {
          window.top.CMS.API.Sideframe.close();
        }
      } catch (err) {}

      if (keepSideFrame) {
        var body = window.document.body;
      } else {
        var body = window.top.document.body;
      }

      fakeForm.appendTo(body).submit();
    };

    $('.js-action, .cms-js-publish-btn, .cms-js-edit-btn, .cms-action-burger-options-anchor').on('click', fakeForm);
    $('.js-close-sideframe').on('click', function () {
      try {
        window.top.CMS.API.Sideframe.close();
      } catch (e) {}
    });
  });
})(typeof django !== 'undefined' && django.jQuery || typeof CMS !== 'undefined' && CMS.$ || false);

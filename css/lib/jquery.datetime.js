/* 
 * Copyright (c) 2009 Marc Hörsken <info@marc-hoersken.de>
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
/* 
 * The Date.setISO8601 function was created by Paul Sowden, thanks a lot!
 * http://delete.me.uk/2005/03/iso8601.html
 */
Date.prototype.setISO8601 = function(string) {
  var regexp = "([0-9]{4})(-([0-9]{2})(-([0-9]{2})" +
      "(T([0-9]{2}):([0-9]{2})(:([0-9]{2})(\.([0-9]+))?)?" +
      "(Z|(([-+])([0-9]{2}):([0-9]{2})))?)?)?)?";
  var d = string.match(new RegExp(regexp));
  
  var offset = 0;
  var date = new Date(d[1], 0, 1);
  
  if (d[3]) { date.setMonth(d[3] - 1); }
  if (d[5]) { date.setDate(d[5]); }
  if (d[7]) { date.setHours(d[7]); }
  if (d[8]) { date.setMinutes(d[8]); }
  if (d[10]) { date.setSeconds(d[10]); }
  if (d[12]) { date.setMilliseconds(Number("0." + d[12]) * 1000); }
  if (d[14]) {
    offset = (Number(d[16]) * 60) + Number(d[17]);
    offset *= ((d[15] == '-') ? 1 : -1);
  }
  
  offset -= date.getTimezoneOffset();
  time = (Number(date) + (offset * 60 * 1000));
  this.setTime(Number(time));
  
  return this;
};
jQuery.removeTimezone = function(string) {
  return string.replace(/\s[A-Z]{3,4}(\+[0-9]{4})?/, '').replace(/\s\([\s\w]+\)/, '');
}
jQuery.fn.extend({
  formatDatetime: function() {
    jQuery(this).find('abbr.d[title]').each(function(i) {
      jQuery(this).text(jQuery.removeTimezone(new Date().setISO8601(jQuery(this).attr('title')).toDateString()));
      jQuery(this).removeClass('d');
    });
    jQuery(this).find('abbr.t[title]').each(function(i) {
      jQuery(this).text(jQuery.removeTimezone(new Date().setISO8601(jQuery(this).attr('title')).toTimeString()));
      jQuery(this).removeClass('t');
    });
    jQuery(this).find('abbr.dt[title]').each(function(i) {
      jQuery(this).text(jQuery.removeTimezone(new Date().setISO8601(jQuery(this).attr('title')).toString()));
      jQuery(this).removeClass('dt');
    });
    jQuery(this).find('abbr.ld[title]').each(function(i) {
      jQuery(this).text(jQuery.removeTimezone(new Date().setISO8601(jQuery(this).attr('title')).toLocaleDateString()));
      jQuery(this).removeClass('ld');
    });
    jQuery(this).find('abbr.lt[title]').each(function(i) {
      jQuery(this).text(jQuery.removeTimezone(new Date().setISO8601(jQuery(this).attr('title')).toLocaleTimeString()));
      jQuery(this).removeClass('lt');
    });
    jQuery(this).find('abbr.ldt[title]').each(function(i) {
      jQuery(this).text(jQuery.removeTimezone(new Date().setISO8601(jQuery(this).attr('title')).toLocaleString()));
      jQuery(this).removeClass('ldt');
    });
    return jQuery(this);
  }
});
jQuery(document).ready(function() {
  jQuery(document).formatDatetime();
});
jQuery(document).ajaxComplete(function(request, settings) {
  jQuery(document).formatDatetime();
});

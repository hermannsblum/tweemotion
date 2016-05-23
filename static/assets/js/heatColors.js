// rolling mean computations

// INITIALISATIONS

Array.prototype.sum = Array.prototype.sum || function() {
  return this.reduce(function(sum, a) { return sum + Number(a) }, 0);
}
Array.prototype.average = Array.prototype.average || function() {
  if (this.length > 1) {
    return this.sum() / (this.length || 1);
  } else {
    // no sentiemnt values yet, return 5
    return 5.0;
  }
}
Array.prototype.update = function(v) {
  // add a new sentiment value to the array
  // if array has more then 30 values, remove the oldest 
  this.push(v);

  if (this.length > 30) {
    // remove oldest value
    this.shift();
  }

  return this.average()
}

// set up an array for all states
var stateSentiments = {
    "AL": [],
    "AZ": [],
    "AR": [],
    "CA": [],
    "CO": [],
    "CT": [],
    "DE": [],
    "DC": [],
    "FL": [],
    "GA": [],
    "HI": [],
    "ID": [],
    "IL": [],
    "IN": [],
    "IA": [],
    "KS": [],
    "KY": [],
    "LA": [],
    "ME": [],
    "MD": [],
    "MA": [],
    "MI": [],
    "MN": [],
    "MS": [],
    "MO": [],
    "MT": [],
    "NE": [],
    "NV": [],
    "NH": [],
    "NJ": [],
    "NM": [],
    "NY": [],
    "NC": [],
    "ND": [],
    "OH": [],
    "OK": [],
    "OR": [],
    "PA": [],
    "PR": [],
    "RI": [],
    "SC": [],
    "SD": [],
    "TN": [],
    "TX": [],
    "UT": [],
    "VT": [],
    "VA": [],
    "WA": [],
    "WV": [],
    "WI": [],
    "WY": []
};


// color calculations

function heatColor(sentiment)  {
    var h = 0.33 * sentiment / 9;
    var l = 0.5 - 0.2 * sentiment / 9;
    return hslToHex(h, 1, l);
}


var componentToHex = function(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
};

/**
 * Converts an HSL color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes h, s, and l are contained in the set [0, 1] and
 * returns r, g, and b as HEX.
 *
 * @param   Number  h       The hue
 * @param   Number  s       The saturation
 * @param   Number  l       The lightness
 * @return  Array           The RGB representation
 */
var hslToHex = function(h, s, l){
    var r, g, b;

    if(s === 0){
        r = g = b = l; // achromatic
    }else{
        var hue2rgb = function hue2rgb(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        };

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    r_hex = componentToHex(Math.round(r * 255));
    g_hex = componentToHex(Math.round(g * 255));
    b_hex = componentToHex(Math.round(b * 255));
    return '#' + r_hex + g_hex + b_hex;
};

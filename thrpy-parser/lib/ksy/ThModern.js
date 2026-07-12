// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['kaitai-struct/KaitaiStream'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('kaitai-struct/KaitaiStream'));
  } else {
    root.ThModern = factory(root.KaitaiStream);
  }
}(typeof self !== 'undefined' ? self : this, function (KaitaiStream) {
var ThModern = (function() {
  function ThModern(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  ThModern.prototype._read = function() {
    this.main = new Main(this._io, this, this._root);
    this.userdata = new Userdata(this._io, this, this._root);
  }

  var Main = ThModern.Main = (function() {
    function Main(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Main.prototype._read = function() {
      this.magicVer = this._io.readU4le();
      this.version = this._io.readU4le();
      this.unused1 = this._io.readU4le();
      this.userdataOffset = this._io.readU4le();
      this.unused2 = this._io.readBytes(12);
      this.compSize = this._io.readU4le();
      this.size = this._io.readU4le();
      this.compData = this._io.readBytes(this.compSize);
    }

    return Main;
  })();

  var Userdata = ThModern.Userdata = (function() {
    function Userdata(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Userdata.prototype._read = function() {
      this.magicUser = this._io.readBytes(4);
      if (!((KaitaiStream.byteArrayCompare(this.magicUser, [85, 83, 69, 82]) == 0))) {
        throw new KaitaiStream.ValidationNotEqualError([85, 83, 69, 82], this.magicUser, this._io, "/types/userdata/seq/0");
      }
      this.userLength = this._io.readU4le();
      this.unknown = this._io.readBytes(4);
      this.userDesc = [];
      var i = 0;
      do {
        var _ = this._io.readU1();
        this.userDesc.push(_);
        i++;
      } while (!(_ == 13));
      this.userDescTerm = KaitaiStream.bytesToStr(this._io.readBytesTerm(10, false, true, true), "ASCII");
      this.userVer = new Crlfstring(this._io, this, this._root);
      this.name = new UserdataField(this._io, this, this._root);
      this.date = new UserdataField(this._io, this, this._root);
      this.shot = new UserdataField(this._io, this, this._root);
      this.difficulty = new UserdataField(this._io, this, this._root);
      this.stage = new Crlfstring(this._io, this, this._root);
      this.score = new UserdataField(this._io, this, this._root);
      this.slowdown = new UserdataField(this._io, this, this._root);
    }

    return Userdata;
  })();

  var Crlfstring = ThModern.Crlfstring = (function() {
    function Crlfstring(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Crlfstring.prototype._read = function() {
      this.value = KaitaiStream.bytesToStr(this._io.readBytesTerm(13, false, true, true), "SJIS");
      this.term = this._io.readU1();
    }

    return Crlfstring;
  })();

  var UserdataField = ThModern.UserdataField = (function() {
    function UserdataField(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    UserdataField.prototype._read = function() {
      this.name = KaitaiStream.bytesToStr(this._io.readBytesTerm(32, false, true, true), "ASCII");
      this.value = KaitaiStream.bytesToStr(this._io.readBytesTerm(13, false, true, true), "ASCII");
      this.term = this._io.readU1();
    }

    return UserdataField;
  })();

  return ThModern;
})();
return ThModern;
}));

// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['kaitai-struct/KaitaiStream'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('kaitai-struct/KaitaiStream'));
  } else {
    root.Th08Userdata = factory(root.KaitaiStream);
  }
}(typeof self !== 'undefined' ? self : this, function (KaitaiStream) {
var Th08Userdata = (function() {
  function Th08Userdata(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  Th08Userdata.prototype._read = function() {
    this.magic = this._io.readBytes(4);
    if (!((KaitaiStream.byteArrayCompare(this.magic, [84, 56, 82, 80]) == 0))) {
      throw new KaitaiStream.ValidationNotEqualError([84, 56, 82, 80], this.magic, this._io, "/seq/0");
    }
    this.version = this._io.readBytes(2);
    this.unknown = this._io.readBytes(6);
    this.userdataOffset = this._io.readU4le();
  }

  var Userdata = Th08Userdata.Userdata = (function() {
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
      this.name = new UserdataField(this._io, this, this._root);
      this.date = new UserdataField(this._io, this, this._root);
      this.shot = new UserdataField(this._io, this, this._root);
      this.score = new UserdataField(this._io, this, this._root);
      this.difficulty = new UserdataField(this._io, this, this._root);
      this.cleared = new UserdataField(this._io, this, this._root);
      this.mistakes = new UserdataField(this._io, this, this._root);
      this.bombs = new UserdataField(this._io, this, this._root);
      this.slowdown = new UserdataField(this._io, this, this._root);
    }

    return Userdata;
  })();

  var Crlfstring = Th08Userdata.Crlfstring = (function() {
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

  var UserdataField = Th08Userdata.UserdataField = (function() {
    function UserdataField(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    UserdataField.prototype._read = function() {
      this.name = KaitaiStream.bytesToStr(this._io.readBytesTerm(9, false, true, true), "SJIS");
      this.value = KaitaiStream.bytesToStr(this._io.readBytesTerm(13, false, true, true), "SJIS");
      this.term = this._io.readU1();
    }

    return UserdataField;
  })();
  Object.defineProperty(Th08Userdata.prototype, 'userdata', {
    get: function() {
      if (this._m_userdata !== undefined)
        return this._m_userdata;
      var _pos = this._io.pos;
      this._io.seek(this.userdataOffset);
      this._m_userdata = new Userdata(this._io, this, this._root);
      this._io.seek(_pos);
      return this._m_userdata;
    }
  });

  return Th08Userdata;
})();
return Th08Userdata;
}));

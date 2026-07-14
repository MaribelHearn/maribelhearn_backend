// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['exports', 'kaitai-struct/KaitaiStream'], factory);
  } else if (typeof exports === 'object' && exports !== null && typeof exports.nodeType !== 'number') {
    factory(exports, require('kaitai-struct/KaitaiStream'));
  } else {
    factory(root.Th20 || (root.Th20 = {}), root.KaitaiStream);
  }
})(typeof self !== 'undefined' ? self : this, function (Th20_, KaitaiStream) {
var Th20 = (function() {
  function Th20(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  Th20.prototype._read = function() {
    this.header = new Header(this._io, this, this._root);
  }

  var Header = Th20.Header = (function() {
    function Header(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root;

      this._read();
    }
    Header.prototype._read = function() {
      this.name = KaitaiStream.bytesToStr(KaitaiStream.bytesTerminate(this._io.readBytes(16), 0, false), "Shift_JIS");
      this.timestamp = this._io.readU8le();
      this.score = this._io.readU4le();
      this.unknown1 = this._io.readBytes(180);
      this.slowdown = this._io.readF4le();
      this.stageCount = this._io.readU4le();
      this.shot = this._io.readU4le();
      this.stones = [];
      for (var i = 0; i < 4; i++) {
        this.stones.push(this._io.readU4le());
      }
      this.unknown2 = this._io.readBytes(4);
      this.difficulty = this._io.readU4le();
      this.unknown3 = this._io.readBytes(4);
      this.unknown4 = this._io.readBytes(4);
      this.spellPracticeId = this._io.readU4le();
    }

    return Header;
  })();

  return Th20;
})();
Th20_.Th20 = Th20;
});

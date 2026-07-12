// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['kaitai-struct/KaitaiStream'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('kaitai-struct/KaitaiStream'));
  } else {
    root.Th128 = factory(root.KaitaiStream);
  }
}(typeof self !== 'undefined' ? self : this, function (KaitaiStream) {
var Th128 = (function() {
  function Th128(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  Th128.prototype._read = function() {
    this.header = new Header(this._io, this, this._root);
    this.stages = [];
    for (var i = 0; i < this.header.stageCount; i++) {
      this.stages.push(new Stage(this._io, this, this._root));
    }
  }

  var Header = Th128.Header = (function() {
    function Header(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Header.prototype._read = function() {
      this.name = KaitaiStream.bytesToStr(KaitaiStream.bytesTerminate(this._io.readBytes(12), 0, false), "SJIS");
      this.timestamp = this._io.readU8le();
      this.score = this._io.readU4le();
      this.unknown1 = this._io.readBytes(60);
      this.slowdown = this._io.readF4le();
      this.stageCount = this._io.readU4le();
      this.route = this._io.readU4le();
      this.subshotUnused = this._io.readU4le();
      this.difficulty = this._io.readU4le();
      this.cleared = this._io.readU4le();
      this.unknown2 = this._io.readBytes(4);
    }

    return Header;
  })();

  var Stage = Th128.Stage = (function() {
    function Stage(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Stage.prototype._read = function() {
      this.stageNum = this._io.readU2le();
      this.seed = this._io.readU2le();
      this.frames = this._io.readU4le();
      this.stageSize = this._io.readU4le();
      this.score = this._io.readU4le();
      this.unknown0 = this._io.readU4le();
      this.piv = this._io.readU4le();
      this.unknown1 = this._io.readBytes(8);
      this.continues = this._io.readU4le();
      this.unknown2 = this._io.readBytes(4);
      this.graze = this._io.readU4le();
      this.unknown3 = this._io.readBytes(84);
      this.motivation = this._io.readU4le();
      this.perfectFreeze = this._io.readU4le();
      this.frozenArea = this._io.readF4le();
      this.unused1 = this._io.readBytes(4);
      this.stageData = this._io.readBytes(this.stageSize);
    }

    return Stage;
  })();

  return Th128;
})();
return Th128;
}));

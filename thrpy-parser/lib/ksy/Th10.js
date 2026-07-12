// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['kaitai-struct/KaitaiStream'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('kaitai-struct/KaitaiStream'));
  } else {
    root.Th10 = factory(root.KaitaiStream);
  }
}(typeof self !== 'undefined' ? self : this, function (KaitaiStream) {
var Th10 = (function() {
  function Th10(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  Th10.prototype._read = function() {
    this.header = new Header(this._io, this, this._root);
    this.stages = [];
    for (var i = 0; i < this.header.stageCount; i++) {
      this.stages.push(new Stage(this._io, this, this._root));
    }
  }

  var Header = Th10.Header = (function() {
    function Header(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Header.prototype._read = function() {
      this.name = KaitaiStream.bytesToStr(this._io.readBytes(12), "SJIS");
      this.timestamp = this._io.readU4le();
      this.score = this._io.readU4le();
      this.unknown1 = this._io.readBytes(52);
      this.slowdown = this._io.readF4le();
      this.stageCount = this._io.readU4le();
      this.shot = this._io.readU4le();
      this.subshot = this._io.readU4le();
      this.difficulty = this._io.readU4le();
      this.unknown3 = this._io.readU4le();
      this.unknown4 = this._io.readU4le();
    }

    return Header;
  })();

  var Stage = Th10.Stage = (function() {
    function Stage(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Stage.prototype._read = function() {
      this.stageNum = this._io.readU2le();
      this.unknown1 = this._io.readU2le();
      this.unknown2 = this._io.readU4le();
      this.nextStageOffset = this._io.readU4le();
      this.score = this._io.readU4le();
      this.power = this._io.readU4le();
      this.piv = this._io.readU4le();
      this.unknown3 = this._io.readU4le();
      this.lives = this._io.readU4le();
      this.restOfHeader = this._io.readBytes(420);
      this.stageData = this._io.readBytes(this.nextStageOffset);
    }

    /**
     * add to current stage offset, + current stage header length which is 0x1c4
     */

    return Stage;
  })();

  return Th10;
})();
return Th10;
}));

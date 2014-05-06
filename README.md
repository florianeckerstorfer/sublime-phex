Phex for Sublime Text
=====================

Phex extends the PHP support provided by Sublime Text 3. It adds additional snippets (PSR-comptabile), extended syntax highlighting and useful commands. Currently there is no possibility to extend the `PHP.tmlanguage`, therefore this is a replacement instead of an addition.


Installation
------------

First you have to disable the default `PHP` package in your preferences:

    {
        ...
        "ignored_packages": [ "PHP" ],
        ...
    }

Then navigate into your `Packages` directory and clone this repository:

    $ git clone https://github.com/florianeckerstorfer/sublime-phex phex


Commands
--------

Phex contains some commands to make it easier for you to work with PHP.

### Create Class

The *Create Class* command allows you to create a new PHP class. This currently only works if you are working in a project. By default the class is created based on the project root folder and if there is a `src` folder in your project root this will be used as base. You can prefix the class with `~` to create the class in the currently active directory, that is, in the directory of the open file.

![Create Class Screencast](https://raw.github.com/florianeckerstorfer/sublime-phex/master/docs/img/create-class.gif)

Phex's *Create Class* command supports PSR-4, except when using relative names (`~` operator). Suppose the following `composer.json` exists in the project root directory:

```json
{
    "autoload": {
        "psr-4": {
            "Phex\\": "src"
        }
    }
}
```

Invoking the *Create Class* command with `Phex\Foo\Bar` creates a class with the following properties:

- Class name: `Bar`
- Namespace: `Phex\Foo\Bar`
- Filename: `src/Foo/Bar.php`

![Create PSR-4 Class Screencast](https://raw.github.com/florianeckerstorfer/sublime-phex/master/docs/img/create-class-psr-4.gif)

### Create Interface

Works like the *Create Class* command, but creates an interface instead of a class.

![Create Interface Screencast](https://raw.github.com/florianeckerstorfer/sublime-phex/master/docs/img/create-interface.gif)

### Insert Class Name

The *Insert Class Name* command opens a fuzzy search panel allowing you to select a class and insertes the selected
class into the view. This command also works outside of the PHP scope and therefore helps you when writing
PHPDoc or other documentation files.

![Insert Class Name Screencast](https://raw.github.com/florianeckerstorfer/sublime-phex/master/docs/img/insert-class-name.gif)

### Insert Namespace

The *Insert Namespace* command inserts the namespace statement of the active file. I recommend setting up a keyboard shortcut, for example, `Super+Alt+n`. You can do this by going to the *Preferences* menu and selecting *Key Bindings - User*. Insert the following snippet:

```json
[
    // Other key bindings
    {
        "keys": ["super+alt+n"], "command": "phex_insert_namespace"
    }
]
```

Configuration
-------------

Phex supports multiple levels of configuration. Currently you can set the author, license and copyright information used by Phex in the PHPDoc when creating new classes and interfaces. You can set your default system settings by creating a file called `phex.sublime-settings` in Sublime's `User/` directory.

For example, this file could look like:

```json
{
    "phex_default_author": "Florian Eckerstorfer <florian@eckerstorfer.co>",
    "phex_default_license": "http://opensource.org/licenses/MIT The MIT License",
    "phex_default_copyright": "(c) 2014 Florian Eckerstorfer"
}
```

Additionally you can change these settings on a per-project basis. Your `.sublime-project` file could look like:

```json
{
    "folders": [
        // ...
    ],
    "settings": {
        "author": "Florian Eckerstorfer",
        "copyright": "2014 Florian Eckerstorfer",
        "license": "http://opensource.org/licenses/MIT The MIT License"
    }
}
```

*Note:* You need to open the project in order to allow Phex to access these settings. If you open the directory (for example, by using the command line helper `subl dir_name`) Phex cannot access the settings and will fall back to the global settings.

Snippets
--------

PHP Extended contains all snippets from the default PHP package from Sublime Text 3 (some slightly modified to match the
Symfony 2 coding standard) and adds new snippets.

The snippets are designed to be as short as possible and still intuitive.

In this documentation the snippets are organized by area of usage: methods, properties, variables and PHPDoc.

### Methods

Snippets to create methods

<table>
    <thead>
        <tr>
            <th>Tab trigger</th>
            <th>Content</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>pufun</code></td>
            <td><code>public function A(B) { … }</code></td>
        </tr>
        <tr>
            <td><code>pofun</code></td>
            <td><code>protected function A(B) { … }</code></td>
        </tr>
        <tr>
            <td><code>pifun</code></td>
            <td><code>private function A(B) { … }</code></td>
        </tr>
        <tr>
            <td><code>pusfun</code></td>
            <td><code>public static function A(B) { … }</code></td>
        </tr>
        <tr>
            <td><code>posfun</code></td>
            <td><code>protected static function A(B) { … }</code></td>
        </tr>
        <tr>
            <td><code>pisfun</code></td>
            <td><code>private static function A(B) { … }</code></td>
        </tr>
    </tbody>
</table>

### Properties

Snippets to create properties.

<table>
    <thead>
        <tr>
            <th>Tab trigger</th>
            <th>Content</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>set</code></td>
            <td><code>public function setA($A) { $this->A = $A; return $this; }</code></td>
        </tr>
        <tr>
            <td><code>get</code></td>
            <td><code>public function getA() { return $this->A; }</code></td>
        </tr>
        <tr>
            <td><code>setget</code></td>
            <td>
                <code>public function setA($A) { $this->A = $A; return $this; }</code>
                <code>public function getA() { return $this->A; }</code>
            </td>
        </tr>
        <tr>
            <td><code>puv</code></td>
            <td><code>public $var;</code></td>
        </tr>
        <tr>
            <td><code>pov</code></td>
            <td><code>protected $var;</code></td>
        </tr>
        <tr>
            <td><code>piv</code></td>
            <td><code>private $var;</code></td>
        </tr>
        <tr>
            <td><code>pusv</code></td>
            <td><code>public static $var;</code></td>
        </tr>
        <tr>
            <td><code>posv</code></td>
            <td><code>protected static $var;</code></td>
        </tr>
        <tr>
            <td><code>pisv</code></td>
            <td><code>private static $var;</code></td>
        </tr>
    </tbody>
</table>

### Variables

Snippets to create and access variables.

<table>
    <thead>
        <tr>
            <th>Tab trigger</th>
            <th>Content</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>rth</code></td>
            <td><code>return $this;</code></td>
        </tr>
        <tr>
            <td><code>-></code></td>
            <td><code>$this->var = $var;</code></td>
        </tr>
        <tr>
            <td><code>ptr</code></td>
            <td><code>print_r($var);</code></td>
        </tr>
        <tr>
            <td><code>preptr</code></td>
            <td><code>echo '&lt;pre&gt;'.print_r($var, true).'&lt;/pre&gt;';</code></td>
        </tr>
        <tr>
            <td><code>vd</code></td>
            <td><code>var_dump($var);</code></td>
        </tr>
        <tr>
            <td><code>prevd</code></td>
            <td><code>echo '&lt;pre&gt;'; var_dump($var); echo '&lt;/pre&gt;';</code></td>
        </tr>
    </tbody>
</table>

### PHPDoc

Snippets for PHPDoc.

<table>
    <thead>
        <tr>
            <th>Tab trigger</th>
            <th>Content</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>indoc</code></td>
            <td><code>/** {@inheritDoc} */</code></td>
        </tr>
    </tbody>
</table>


Syntax Highlighting
-------------------

Currently Phex extends the syntax highlighting provided by the default PHP package. I hope to extend this in the future.

### Annotations

The default `PHP.tmlanguage` only has support for PHPDoc annotations. Phex adds support for popular libraries
and their annotations.

#### Doctrine MongoDB ODM

Phex has syntax highlighting for annotations provided by
[Doctrine MongoDB ODM](http://www.doctrine-project.org/projects/mongodb-odm.html).

- `MongoDB\AlsoLoad`
- `MongoDB\Bin`
- `MongoDB\BinCustom`
- `MongoDB\BinFunc`
- `MongoDB\BinMD5`
- `MongoDB\BinUUID`
- `MongoDB\Boolean`
- `MongoDB\Collection`
- `MongoDB\Date`
- `MongoDB\DiscriminatorField`
- `MongoDB\DiscriminatorMap`
- `MongoDB\Distance`
- `MongoDB\Document)`
- `MongoDB\EmbedMany`
- `MongoDB\EmbedOne`
- `MongoDB\EmbeddedDocument`
- `MongoDB\Field`
- `MongoDB\File`
- `MongoDB\Float`
- `MongoDB\Hash`
- `MongoDB\Id`
- `MongoDB\Increment`
- `MongoDB\Index`
- `MongoDB\Int`
- `MongoDB\InheritanceType`
- `MongoDB\Key`
- `MongoDB\MappedSuperclass`
- `MongoDB\NotSaved`
- `MongoDB\PostLoad`
- `MongoDB\PostPersist`
- `MongoDB\PostRemove`
- `MongoDB\PostUpdate`
- `MongoDB\PreLoad`
- `MongoDB\PrePersist`
- `MongoDB\PreRemove`
- `MongoDB\PreUpdate`
- `MongoDB\ReferenceMany`
- `MongoDB\ReferenceOne`
- `MongoDB\String`
- `MongoDB\Timestamp`
- `MongoDB\UniqueIndex`

#### Doctrine ORM

Phex has syntax highlighting for annotations provided by [Doctrine ORM](http://www.doctrine-project.org/projects/orm).

- `ORM\Column`
- `ORM\ChangeTrackingPolicy`
- `ORM\|DiscriminatorColumn`
- `ORM\|DiscriminatorMap`
- `ORM\Entity`
- `ORM\GeneratedValue`
- `ORM\HasLifecycleCallbacks`
- `ORM\Id`
- `ORM\Index`
- `ORM\InheritanceType`
- `ORM\JoinColumn`
- `ORM\JoinColumns`
- `ORM\JoinTable`
- `ORM\ManyToOne`
- `ORM\ManyToMany`
- `ORM\MappedSuperclass`
- `ORM\OneToOne`
- `ORM\OneToMany`
- `ORM\OrderBy`
- `ORM\PostLoad`
- `ORM\PostPersist`
- `ORM\PostRemove`
- `ORM\PostUpdate`
- `ORM\PrePersist`
- `ORM\PreRemove`
- `ORM\PreUpdate`
- `ORM\SequenceGenerator`
- `ORM\Table`
- `ORM\UniqueConstraint`
- `ORM\Version`

#### Symfony2 Validation

Phex has syntax highlighting for annotations provided by
[Symfony2 Validation](http://symfony.com/doc/current/book/validation.html).

- `Assert\All`
- `Assert\Blank`
- `Assert\Callback`
- `Assert\Choice`
- `Assert\Collection`
- `Assert\Country`
- `Assert\Date`
- `Assert\DateTime`
- `Assert\Email`
- `Assert\False`
- `Assert\File`
- `Assert\Image`
- `Assert\Ip`
- `Assert\Language`
- `Assert\Length`
- `Assert\Locale`
- `Assert\Min`
- `Assert\MinLength`
- `Assert\Max`
- `Assert\MaxLength`
- `Assert\NotBlank`
- `Assert\NotNull`
- `Assert\Null`
- `Assert\Regex`
- `Assert\Time`
- `Assert\True`
- `Assert\Type`
- `Assert\Url`
- `Assert\Valid`
- `UniqueEntity`

#### PHPUnit

Phex has syntax highlighting for annotations provided by [PHPUnit](https://github.com/sebastianbergmann/phpunit/).

- `assert`
- `backupGlobals`
- `backupStaticAttributes`
- `codeCoverageIgnore`
- `codeCoverageIgnoreStart`
- `codeCoverageIgnoreEnd`
- `covers`
- `dataProvider`
- `depends`
- `expectedException`
- `expectedExceptionCode`
- `expectedExceptionMessage`
- `group`
- `outputBuffering`
- `runTestsInSeparateProcesses`
- `runInSeparateProcess`
- `test`
- `testdox`
- `ticket`

#### Gedmo Doctrine Extensions

Phex has syntax highlighting for annotations provided by
[Gedmo Doctrine Extensions](https://github.com/l3pp4rd/DoctrineExtensions).

- `Gedmo\Slug`
- `Gedmo\SoftDeleteable`
- `Gedmo\Timestampable`
- `Gedmo\Translatable`

#### Braincrafted Validation

Phex has syntax highlighting for annotations provided by
[Braincrafted Validation](https://github.com/braincrafted/validation-bundle).

- `BraincraftedAssert\Enum`


Author
------

- [Florian Eckerstorfer](http://florian.ec) ([Twitter](http://twitter.com/Florian_), [App.net](http://app.net/florian))

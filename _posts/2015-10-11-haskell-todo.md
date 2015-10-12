---
title: "Basic Haskell: an examination of the todo list"
permalink: /basic-haskell-todo/
layout: post
published: true
date: 2015-10-11
teaser: >
    A teardown of a basic Haskell example, with line by line
    explanations of what and why. No warranty as to correctness.
---

The prolific Gabriel Gonzalez wrote a post last week about
[basic Haskell
examples](http://www.haskellforall.com/2015/10/basic-haskell-examples.html).
Regarding the state of example Haskell code, often using advanced langauge
idioms:

> So I would like to swing the pendulum in the other direction by just
> writing five small but useful programs without any imports, language
> extensions, or advanced features. These are programs that you could
> write in any other language and that's the point: you can use Haskell
> in the same way that you use other languages.

Followed by five examples:

1. a todo program
2. a TSV to CSV converter
3. a calendar printing utility
4. an RNA decoder
5. a bedtime story generator

I imagine 4 & 5 could be combined in some way for very precocious children.

Haskell has had my interest for a while but I've made far less progress
learning the language than seems reasonable for someone who can tie his own
shoes, in no small part because it's much more
difficult to get started doing anything productive compared to a host of
other languages. It's a much more
interesting language than Go, for example, but Go fulfills it's promise of
programmer productivity almost immediately. The resolution, for me at least, is to
find basic programs that actually *do things* (i.e. IO). So for my own
benefit, and perhaps yours, too, if you're in my boat, is to work with
these examples, explaining and extending to the more uniquely usable
tools.

I'm going to examine the todo example and walk through it line by line to
examine and explain what it's doing. Keep in mind that unlike Haskell I make no
claims on my own correctness (my mother would be surprised to hear that, I'm
sure). That includes explanation of concept as well as my language, which
is almost certainly insufficiently precise even when it is accurate.

Here's the full example as originally presented (the code on Gabriel's
site has been updated a bit). In my walkthrough I've rearragned the
order to start with the entry point and go from there.

```haskell
putTodo :: (Int, String) -> IO ()
putTodo (n, todo) = putStrLn (show n ++ ": " ++ todo)

prompt :: [String] -> IO ()
prompt todos = do
    putStrLn ""
    putStrLn "Current TODO list:"
    mapM_ putTodo (zip [0..] todos)
    command <- getLine
    interpret command todos

interpret :: String -> [String] -> IO ()
interpret ('+':' ':todo) todos = prompt (todo:todos)
interpret ('-':' ':num ) todos =
    case delete (read num) todos of
        Nothing -> do
            putStrLn "No TODO entry matches the given number"
            prompt todos
        Just todos' -> prompt todos'
interpret  "q"           todos = return ()
interpret  command       todos = do
    putStrLn ("Invalid command: `" ++ command ++ "`")
    prompt todos

delete :: Int -> [a] -> Maybe [a]
delete 0 (_:as) = Just as
delete n (a:as) = do
    let n' = n - 1
    as' <- n' `seq` delete n' as
    return (a:as')
delete _  []    = Nothing

main = do
    putStrLn "Commands:"
    putStrLn "+ <String> - Add a TODO entry"
    putStrLn "- <Int>    - Delete the numbered entry"
    putStrLn "q          - Quit"
    prompt []
```

## Do something: the entrypoint

A program is useless if you can't do anything with it, and every Haskell
program has a `main` function. In the example it's written at the bottom of the
Haskell code, and while that's a reasonable and typical place for an entrypoint
in other languages, too, it's going to be our starting point.

```haskell
main = do
    putStrLn "Commands:"
    putStrLn "+ <String> - Adda TODO entry"
    putStrLn "- <Int>    - Delete the numbered entry"
    putStrLn "q          - Quit"
    prompt []
```

The first line assigns some stuff to `main` with a `do` statement. Here's what
I know about `do`: it's syntactic sugar around monadic code which could be
rewritten without the `do` statement; writing the monadic code is makes it
clearer if you understand it, but the `do` statement looks nicer for us folks
more used to imperative paradigms. I'm pretty sure this is true because I read
it on the Internet.

Monadic means related to monads. And a monad is either a burrito or a calzone.
A *little* bit more on this later.

The next four lines are function calls to the `putStrLn` function. In the
context of this `do` block this is pretty obvious to the unitiated: the
function prints the string argument to the screen. Of course that's only
superficially true - that is, it describes what happens, but doesn't really
describe the `putStrLn` function. Output is a side effect, so how can a
function do that?

As defined in [the] Prelude (what's available without import in Haskell),
`putStrLn` has the following type signature:

```haskell
putStrLn :: String -> IO ()
```

I'm sure that clears it right up. It says that the function takes an argument
of type `String` and returns an IO monad. It prints to the screen with a new
line, where as `putStr` simply prints the string without a newline. `putStr` is
to `putStrLn` as Ruby's `print` is to `puts`, roughly.

The last line of the `main` function calls the `prompt` function an empty list.

### do or then

As I mentioned, it's possible to write this kind of code without using
`do`. Here's the `main` function written without the benefit of `do`
notation.

```haskell
main =
    putStrLn "Commands:" >>
    putStrLn "+ <String> - Adda TODO entry" >>
    putStrLn "- <Int>    - Delete the numbered entry" >>
    putStrLn "q          - Quit" >>
    prompt []
```

The "then" operator is used to chain operations. Here's the type
signature of the `>>` or "then" operator:

```haskell
(>>) :: Monad m => m a -> m b -> m b
```

The description from the Haskell docs is reasonably helpful:

> Sequentially compose two actions, discarding any value produced by the
> first, like sequencing operators (such as the semicolon) in imperative
> languages.

That's exactly what we want to happen here.

### So, what's a monad?

There's a slew of explanations of what a monad is. An infamous attempt
compares [monads to burritos](http://blog.plover.com/prog/burritos.html).
Maybe this makes sense once you grok the concept of monads already, but
I didn't find the explanation terribly helpful.

A monad has a precise definition with regard to category theory, but
better or at least shallower explanations are that monads are sequenced
operations. Functions in Haskell are not sequentially applied, and
monads allow you to do this. They also provide a way out when it comes
to dealing with side effects which a pure functional programming
otherwise prohibits.

My suspicion is that it's possible to get reasonably far reading and
writing Haskell code without fully grokking monads, and that once that
is achieved they won't look half as complicated as they're presented.

For now let's hold that a monad is a type class that sequences
operations - even if that's terribly wrong.

### Type classes

Short aside about type classes: the best analogy for type classes in Python are abstract base classes, or if
you're not familiar with abstact base classes, in practice the use of dunder
methods. For instance you might write a function in Python that iterates over
an object - we call this "iteration" - without needing to know what class the
object is an instance of. It could be a string, a generator object, a class of
your own creation - anything that defines a `__next__` method. So if a class
defines a `__next__` method as well as an `__iter__` method then it's an
iterator. This is conceptually similar to a type class.

Or in Go, an interface.

## Prompt for input

The `prompt` function below is responsible for outputting a prompt to the user,
waiting for input, and then doing something with that input.

```haskell
prompt :: [String] -> IO ()
prompt todos = do
    putStrLn ""
    putStrLn "Current TODO List:"
    mapM_ putTodo (zip [0..] todos)
    command <- getLine
    interpret command todos
```

This function takes a list of `String` instances (which means it's a list of
lists, since a `String` is a list of `Char` instances) and returns an `IO`
monad (calzone). The particular input it's getting for the list of strings is a
list of our todos.

This function uses the `do` notation as well, which is a good indicator that
it's *doing* some IO. The first two lines we can now already understand. The
function is outputting some text. It could be condensed into one line if we
wanted (same in pretty much any language) but the `putStrLn` function call with
the blank string is nicely explicit.

```haskell
putStrLn "\nCurrent TODO List:"
```

### List output by function mapping

The third line of the function is more interesting. Here's the type signature
for `mapM_`:

```haskell
mapM_ :: Monad m => (a -> m b) -> [a] -> m ()
```

Looking across the signature we can see three different type references, `a`,
`b`, and `m`. `m` is the only one with a type class specified; `m` must
implement type class `Monad`. Types `a` and `b` can be any type.

So `mapM_` takes a function and a list and returns a burrito/monad. The function
argument to `mapM_` takes an instance of type `a` and returns a monad of type
`b`. Let's look at how we're using this function and then come back to it.

The `prompt` function calls the `mapM_` function with two parameters: the
`putTodo` function, which is defined later, and the result of calling the `zip`
function on what looks like some kind of auto populating list of numbers
and our list of todos. This part's making a bit more sense. `mapM_` is mapping
the `putTodo` function over the result of the `zip` function.

The `zip` function looks pretty familiar:

```haskell
zip :: [a] -> [b] -> [(a, b)]
```

It takes a list of instances of type `a` and a list of instances of type `b`
and returns a list of tuples each with an instance of type `a` and `b`
respectively. Some implementation of a `zip`-like function is in the standard
libary of every high-level language with [few
exceptions](https://en.wikipedia.org/wiki/JavaScript).

Here `zip` is provided with the aforementioned integer list and our list of
todos. The integer list is constructed with the range syntax `..`. This is
pretty nice, as it can be used to produce a list without verbosely writing it
out.

```haskell
ghci > [1..10]
[1,2,3,4,5,6,7,8,9,10]
```

The neat part is that by leaving off the end of the range, we get an infinite
list! That's sounds like a somewhat scary thing, but here it's of no concern, as
long as todos is finite. That's because given lists of unequal length, `zip`
will produce a list only as long as the shortest input. This is lazy evaluation
at work (if you're working in Python you can often get the same general benefit
by using generators).

The next line is quite short, but introduces new functionality and syntax.

```haskell
command <- getLine
```

The left pointing arrow - certainly how I interpret it - *binds* `getLine` to
`command`. Here's the helpful type signature:

```haskell
getLine :: IO String
```

`getLine` just returns an `IO String`. It doesn't take any arguments, although
it does take some input via IO. That's why it returns an `IO String`. I'm not
entirely sure what's going on under the hood, but it reminds me of using `cin`
in C++:

```cpp
cin >> command;
```

Execution is going to stop until input - marked as finalized by the return key
- is streamed into `command`.

And in the last line, our input in `command` and the todos list are sent as
arguments to the `interpret` function.

## Output a todo item

The `putTodo` function prints to the screen a todo prefaced by it's numeric
index in the list of todos.

```haskell
putTodo :: (Int, String) -> IO ()
putTodo (n, todo) = putStrLn (show n ++ ": " ++ todo)
```

In slightly unidiomatic Python, it would look like this:

```python
def putTodo(n, todo):
    print(n + ": " + todo)
```
So it's not really all *that* different. String concatenation is performed with
the `++` operator, not the `+` operator. Python's `+` operator can be used with
mixed types (thanks, dunder methods!) but we can't do that in Haskell.

Let's look at why. Operators are just infix functions - functions written
between the parameters - so let's look at the type signature for the `+`
operator:

```haskell
(+) :: Num a => a -> a -> a
```

What that shows us is that it takes an instance of type `a` and another
instance of type `a` and returns an instance of type `a`. `a` here is a
placeholder for any type that satisfies the requirements of the `Num` *type
class* (more on that below).

Let's compare to the `++` concatenation operator:

```haskell
(++) :: [a] -> [a] -> [a]
```

Notice that it doesn't specify the type class for `a`. Concatenation
operator don't care. It's operating on the boxes containing type `a`. All that
matters is that the things in each box being concatenated are of the same type.
Lists are expected to hold one type.

Side note: lists *must* hold the same type, but this is a good practice even in
dynamically typed languages like Python. Otherwise you'll sow confusion, write
complicated code, and if you're lucky enjoy some high quality runtime errors.

Since we want a string, we need to coerce the `Int` into a `String`. That's
what `show` does here.

The `show` function has the following type signature:

```haskell
show :: Show a => a -> String
```

That is, it takes an instance of type `a` and returns a `String`. Pretty
simple. As long as the type `a` is of the `Show` type class. One way or
another, type definitions will define the `show` function, declaring the type
to be an instance of `Show`, and this function can be called when the `show`
function is called from the Prelude.

Back to our `putTodo` function, the `show` function uses the `Int` type's
`show` funtion to return a `String` representation of the `Int` value. This can
then be concatenated with the spacer string and the todo itself, and the
resulting `String` is used as a parameter for the `putStrLn` function.

### Parantheses and function parameters

Another sidenote: parantheses are unnecessary for calling functions in Haskell.
When they're used it's either for readability (human's sake) or ensuring
parameters are interpreted correctly (compiler's sake).

If you try to evaluate this code in ghci you'll get a type error:

```haskell
let n = 0
let todo = "Walk the dog"
putStrLn show n ++ ": " ++ todo
```

Thinking as best I can as a compiler, I'd not necessarily recognize the
evaluation order - does `show` need to be evaluated first before calling
`putStrLn`?  - so it needs to be syntactically enforced. An alternative
way of writing this, and seemingly more idiomatic from the Haskell code
I've seen, is to use the `$` operator:

```haskell
putStrLn $ show n ++ ": " ++ todo
```

## Handling user input

Now we get to the engine of the program. It's also our first example using
pattern matching for function definition.

```haskell
interpret :: String -> [String] -> IO ()
interpret ('+':' ':todo) todos = prompt (todo:todos)
interpret ('-':' ':num ) todos =
    case delete (read num) todos of
        Nothing -> do
            putStrLn "No TODO entry matches the given number"
            prompt todos
        Just todos' -> prompt todos'
interpret  "q"          todos = return ()
interpret command       todos = do
    putStrLn ("Invalid command: `" ++ command ++ "`")
    prompt todos
```

Pattern matching is one of those language features that I saw in Haskell and
thought, okay, that looks kind of neat, and then found myself refactoring code
in another language and thought, "$@#! this would be simpler with pattern
matching". Pattern matching allows us to apply function bodies based not just
on the name of the function but on specific argument values. It's implemented
by specifying values of one kind or another in the place of or inserted into
the "shape" of an argument.

```haskell
divide :: Num -> Num -> Num
divide x 0 = 0
divide x y = x / y
```

That's not mathematically sound but it illustrates the point.
And at first it doesn't look that dissimilar from an unnecessary mess, after
all, there's all of these definitions. But it makes for function bodies that
"do" only what they need to, and it's nicer than a rats nest of if statements.

Back to the function itself, it takes a string and a list of strings and it
returns an IO monad.

The first pattern uses a new operator, `:`, to create a string matching the
user input. Here's the type signature for the operator:

```haskell
(:) :: a -> [a] -> [a]
```

It's takes a single element of type class `a`, a list of type class `a`, and
returns a list of type class `a`. The way it's written here works because of
how the arguments are interpreted. Substituting `cons` for `:` and as a non-infix
function, it might look like this in Python:

```python
cons("+", cons(" ", todo))
```

Or more appropriately in Clojure:

```clojure
(cons "+" (cons " " todo))
```

The choice of quotation mark is significant, as well. Single quotes `'` are
used for characters, double quotes `"` for strings. (Also, the `String`
type is just an alias to a list of characters, e.g. `[Char]`.)
If you try this in ghci you'll encounter an error:

```haskell
("+":" ":"My new todo")
```

When the correct pattern is matched here though, a string starting with "+ "
and followed by a non-empty string, then the first function body definition is
used. In that case it simply returns the previously examined `prompt` function,
prepending our new todo to the existing todo list.

Now the second pattern looks quite similar, albeit with a different preface
character and different variable name. That's legal and as you'll notice very
helpful. It's the same type signature, and the name is local to the function
body following this pattern.

The function body introduces the use of `case` which as you mgiht imagine isn't
all that conceptually different from `case` in other languages. Why use `case`
rather than another pattern? Because `case` is applied against the result of a
function call. Now, it's true that the first two patterns are as well, after all,
the `:` operator is a function. However the result of prepending those values
is determinate, whereas the `delete` function returns a `Maybe` value, having
either a value wrapped in a `Just` or a `Nothing`.

As such, if the result of `delete (read num) todos` is `Nothing` then the next
two lines are invoked, and if the result in a list of todos wrapped in a Just,
which gets labeled `todos'`, then the list is used as an argument back to
the `prompt` function.

The `interpret` function can return a call to the `prompt` function because
the latter returns an `IO` monad, just like the former.

The function call in the `case` statement introduces another function, `read`.
Here's the type signature:

```haskell
read :: Read a => String -> a
```

It takes a string as input and returns an `a` where type
`a` implements the `Read` type class. Okay, so that means that the type `a`
must implement a `read` function. Of what use is this?

Well, if you look back to the pattern and the function signature of `:`, we
know that `num` must be a `String`. However `delete` requires an `Int`. The
effect of `read` is to coerce the value of `num` into an `Int`. It's basically
the inverse of `show`.

The third pattern and function body are pretty straightforward. If the entry is
nothing more than a lower case "q" the return value is an empty monad.

The fourth value is akin to the "default" condition in a case statement
(at least in a `C` like language). All of the valid inputs have been handled
so anything else is handled here. The function body consists of another monadic
block in which the user is alerted to their error and then the prompt
function is once again called.

## Remove an item

Lastly we come to the `delete` function. We see pattern matching employed here,
too, and an interesting return value, `Maybe`. This function takes an `Int` and
a list of a type `a` and it returns a list of a type `a` *wrapped* in a
`Maybe`.

```haskell
delete :: Int -> [a] -> Maybe [a]
delete 0 (_:as) = Just as
delete n (a:as) = do
    let n' = n - 1
    as' <- n' `seq` delete n' as
    return (a:as')
delete _ []     = Nothing
```

`Maybe`, e.g. `Maybe Int`, is a way of noting that the value might be an `Int`
or it might be nothing. Just as a list itself could have items or be empty, any
value, whether a collection type or not, can be wrapped in a `Maybe` - either
`Just`, e.g. `Just 5` to indicate that there is an integer which can be
*unwrapped* or *unboxed* from the `Maybe`, or `Nothing`.

This whole `Maybe` business seems to beg the question that this is better than
returning, say, `nil` or `None`. At first pass it doesn't seem any better.
Couldn't you *just* - pardon me, I had to - check for whether the value
returned back is `nil` or length of 0 or something of that sort? You could.
It'd bet a little messier though, just look at pattern matching. This nil or
zero status has to be checked differently for every type. Here we have a
consistent type based wrapper and, bonus, you an use it for pattern matching
(see the `interpret` function).

Speaking of pattern matching, let's look at the function's pattern defintions.
Looking through the different patterns for the function, it becomes clear how
and why each is applied.

The first pattern matches against the first argument as the integer 0, and the
second argument is the list of `a` typed instances. The second argument is
further defined with a range. Here the `:` operator splits the list on the
head, the first item in the list, and the tail, everything after that. These
are named separately and can be referenced in the function body. The `_` for
the head means that it's irrelevant - it's going to be thrown away. If you've
programmed in Go you've seen the same thing. If you've seen this in Python
you've seen an anti-pattern.

The function body for the first pattern returns the tail of the input function.
Well this makes sense! If you want to delete the first item, the 0-indexed
item, in a list, then you should end up with the tail of the original list.

The third pattern (I'm skipping) simply matches an empty list. The index value is totally
irrelevant, no matter what, and the return value is `Nothing`. Looking only at
this pattern, we could have just returned an empty list. However the `Nothing`
value is more generalizable. Any missing value should be treated the same way
in the user interface whether the list is empty or not, and this return value
greatly simplifies that. If a user tries to delete an item from a list, whether
it's missing because it cannot be found or because the list is empty, this
should be handled in the same way.

The second pattern is pretty similar to the first, except that the first
parameter is given a value  name so that it can be referenced (and
meaning that it should match any non-specified value) and the head of the list
is likewise referenced. The second function body definition is quite different.

The `do` keyword tells us that there's some sort of monadic magic at work here.
Looking into the first line of this block it names a value `n'` - the apostrophe
doesn't have any special syntactical meaning to the compiler, it's for the
programmer's benefit - and this named value is assigned n - 1. So if there are
five items in the list, and I want to delete the third item, indexed 2,
then `n'` will have a value of 1.

In the next line there's what briefly looks like another value assignment, but
it's actually a value binding. The left pointing arrow `<-` binds everything to
the right to the value on the left. So what's on the right side?

Notice first the call to `seq` here using backticks ``seq``. Here's the type
signature of `seq`:

```haskell
seq :: a -> b -> b
```

The backticks allow `seq` to be used as in infix function. You can do this with
any function that takes two arguments (subject to restrictions about which I'm
ignorant, so grain of salt on the 'any' there). The `seq` function returns the
second argument, `b`, unless `a` is "bottom" in which case it returns `a`.
Insert head scratching here I supposed.

The Haskell wiki describes `seq` as ["the most basic method of introducing
strictness"](https://wiki.haskell.org/Seq). It seems that it must make a comparison
and so requires that each argument is evaluated. There's some controversy
around this that represents a very fine rabbit hole I've no intention of
investigating right now. At any rate we should look at what "bottom" means here.
The [Haskell wiki introduces bottom](https://wiki.haskell.org/Bottom) thusly:

    The term bottom refers to a computation which never completes successfully. That includes a computation that fails due to some kind of error, and a computation that just goes into an infinite loop (without returning any data).

Note the conditions, that it fails due to an error or a compution that goes
into an infinite loop *without returning any data*. If you try using `seq` in
ghci you can see here you'd get 9.

```haskell
Prelude> seq [0..] 9
True
```

9 is not bottom. Maybe that infinite range is though.

```haskell
Prelude> seq 9 [0..]
[0,1,2,3...]
```

Nope! Hope you hit Ctrl+c. That infinite expansion returns values, so it's not
bottom. Even [`Nothing`](https://www.youtube.com/watch?v=CrG-lsrXKRM) isn't bottom.

```haskell
Prelude> seq 9 Nothing
Nothing
```

In any event, `seq` is used here to compare `n'` and the value of `delete n' as`,
just like so without the infix syntax:

```haskell
seq n' (delete n' as)
```

Let's walk through an example to understand how this recursion is working.
Here's my todo list:

```bash
Current TODO List:
0: Edit blog post
1: Sweep the garage
2: Mow the lawn
3: Make lunch
4: Walk the dog
```

Normally it would involve more adventure, I promise. I'd like to remove the
todo "Mow the lawn" because I hate mowing the lawn. Since I enter `2`, the value
of `n` is `2`, `a` is "Edit blog post" and `as` is a list of the next four todos.

Now `n'` is `1`, and to `as'` we have bound the result of `seq` with values `1`
and `delete 1 as` where `as` is todos starting at index 1. This means another
recursive call to `delete`.

Since `n` is non-zero and the list is non-empty, this once again uses the
second function definition. And now `n'` is 0, the `seq` line with a recursive
call to `delete` is evaluated with `as` equal to the part of the list of todos
starting from the second indexed item, "Mow the lawn", which is the one I want
to delete. The first pattern is now matched against *this* recursive call,
because the `n` value is 0, and the tail of the passed list is returned, in this
case the list starting from the todo *after* the one I wanted to delete.

Going back up the chain of recursion, the value `Just as` where `as` is the last
two items in our list, is bound to `as`.

```bash
Make lunch
Walk the dog
```

The value of `a` is "Sweep the garage", and using the list appending operator
`:` we can effectively put the former head back onto the new tail and return
it.

The `return` statement should look odd, since functions in Haskell neither need
nor use `return`. Instead it is used to "[i]nject a value into the monadic type."
It's synonymous, at least in this case, with this line:

```haskell
Just (a:as')
```

`return` is a function with this type signautre:

```haskell
return :: Monad m => a -> m a
```

Given that `Just` is an instance of `Maybe` which is a `Monad`, we can
see the equivalence - at least in this specific case.
The explicit use of `Just` makes more sense to me, but having seen the `return`
used enough in similar looking blocks of code, it smells like there's probably
a reason to use `return` - I just couldn't tell you what it is.

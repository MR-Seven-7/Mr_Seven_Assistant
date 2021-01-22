# Mr_Seven_Assistant
A small virtual assistant made in Python for a code jam, Timathon, held by TechWithTim.

<strong>Note : To access settings or add commands give 'settings' command.</strong>

<h2> What can it do ?</h2>

<ul>
  <li>It lets you add your command with a <strong>Key-Value</strong>. Where <strong>Key</strong> holds the command through which you want to trigger action which is held by  <strong>Value. </strong>Value</strong> should hold location of the file or terminal command to be executed. You add commands through settings. Example : <br>
    Key = pip<br>
    Value = pip install<br>
    Command = pip install module_name<br>This will pip install the module.<br><br>Or<br><br>
    Key = open code<br>
    Value = location of Visual studio code or its shorcut<br>
    Command = open code<br>
    This will open Visual studio code
    </li>
    Will result in installing the module named python. The value can be any terminal command from shutdown to cd.</li>
    <li>Play music for you. To play music it searches the directory which you can provide using settings, if not found it play it on Youtube. Example : play lose yourself</li>
    <li>Open website for you. Example : 'open techwithtim' will open techwithtim.net</li>
    <li>Search wikipedia. Example : 'what is apple inc' or 'who is steve jobs' or 'wiki youtube'</li>
    <li>Reply to some regular question. Example : 'what is your name' or 'good morning' or 'what is date/time'
  </ul>
  
<h2> How To Use ?</h2>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run main.pyw

<h2> How to know the status ?</h2>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To see status refer to the dot at the last of the window.
Here is what the color of the circle means : <br>
<ul>
  <li>Black : Welcome!</li>
  <li>Blue : Listening or Recognizing your vocal input</li>
  <li>Yellow : Processing command</li>
  <li>Green : Command executed successfully</li>
  <li>Red : Failed to execute command</li>
</ul>
<h2> Buttons </h2>
<ul>
  <li> E : Execute (Enter Key)</li>
  <li> M : Microphone (Tab Key)</li>
  <li> X : Close (Esc Key)</li>
  </ul>
  

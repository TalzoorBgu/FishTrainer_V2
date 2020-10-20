#############################################################################
# Generated by PAGE version 4.24
#  in conjunction with Tcl version 8.6
#  Aug 14, 2019 10:33:33 AM IDT  platform: Darwin
set vTcl(timestamp) ""


if {!$vTcl(borrow)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #d8d8d8
set vTcl(active_menu_fg) #000000
}



if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top37
    global vTcl
    set base $vTcl(btop)
    if {$base == ""} {
        set base .top37
    }
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist {_TopLevel _vTclBalloon}
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}


proc vTclWindow.top37 {base} {
    if {$base == ""} {
        set base .top37
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -menu "$top.m45" -background {#d9d9d9} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 880x748+246+63
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1440 855
    wm minsize $top 120 15
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "Fish training GUI V2 - Client"
    vTcl:DefineAlias "$top" "MainGUI" vTcl:Toplevel:WidgetProc "" 1
    frame $top.fra38 \
        -borderwidth 2 -relief groove -background {#d9d9d9} -height 131 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 654 
    vTcl:DefineAlias "$top.fra38" "frmTraining" vTcl:WidgetProc "MainGUI" 1
    set site_3_0 $top.fra38
    button $site_3_0.but39 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onRunTraining -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text {Run training} -wraplength 50 
    vTcl:DefineAlias "$site_3_0.but39" "btnRunTraining" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab46 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Training day} 
    vTcl:DefineAlias "$site_3_0.lab46" "Label2" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad48 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R1Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text Feed -value F \
        -variable FeedVar1 
    vTcl:DefineAlias "$site_3_0.rad48" "radF1" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad49 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R1Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text {No feed} -value NF \
        -variable FeedVar1 
    vTcl:DefineAlias "$site_3_0.rad49" "radN1" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab50 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text {Fish no.} 
    vTcl:DefineAlias "$site_3_0.lab50" "Label1" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but38 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onStopTraining -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text {Stop training} -wraplength 50 
    vTcl:DefineAlias "$site_3_0.but38" "btnStopTraining" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex45 \
        -background white -font TkTextFont -foreground black -height 32 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 60 -wrap word 
    .top37.fra38.tex45 configure -font "TkTextFont"
    .top37.fra38.tex45 insert end text
    vTcl:DefineAlias "$site_3_0.tex45" "txtFishNo1" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex46 \
        -background white -font TkTextFont -foreground black -height 32 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 42 -wrap word 
    .top37.fra38.tex46 configure -font "TkTextFont"
    .top37.fra38.tex46 insert end text
    vTcl:DefineAlias "$site_3_0.tex46" "txtTrainingDay1" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex42 \
        -background white -font TkTextFont -foreground black -height 32 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 60 -wrap word 
    .top37.fra38.tex42 configure -font "TkTextFont"
    .top37.fra38.tex42 insert end text
    vTcl:DefineAlias "$site_3_0.tex42" "txtFishNo2" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex43 \
        -background white -font TkTextFont -foreground black -height 32 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 42 -wrap word 
    .top37.fra38.tex43 configure -font "TkTextFont"
    .top37.fra38.tex43 insert end text
    vTcl:DefineAlias "$site_3_0.tex43" "txtTrainingDay2" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad44 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R2Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text Feed -value F \
        -variable FeedVar2 
    vTcl:DefineAlias "$site_3_0.rad44" "radF2" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad45 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R2Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text {No feed} -value NF \
        -variable FeedVar2 
    vTcl:DefineAlias "$site_3_0.rad45" "radN2" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad40 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R1Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text {Camera 1} -value 0 \
        -variable CamVar1 
    vTcl:DefineAlias "$site_3_0.rad40" "radCam1" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad41 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R1Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text Feed -value F \
        -variable FeedVar1 
    radiobutton $site_3_0.rad42 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R1Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text Feed -value F \
        -variable FeedVar1 
    radiobutton $site_3_0.rad43 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R1Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text {Camera 2} -value 1 \
        -variable CamVar1 
    vTcl:DefineAlias "$site_3_0.rad43" "radCam2" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but44 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onTankConfig -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text {Tank conf.} 
    vTcl:DefineAlias "$site_3_0.but44" "btnTankConf" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad38 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R3Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text Center -value C \
        -variable TrainingVar 
    vTcl:DefineAlias "$site_3_0.rad38" "radF1_2" vTcl:WidgetProc "MainGUI" 1
    radiobutton $site_3_0.rad39 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command R3Sel -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text Edge -value E \
        -variable TrainingVar 
    vTcl:DefineAlias "$site_3_0.rad39" "radF1_1" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab49 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Training type} 
    vTcl:DefineAlias "$site_3_0.lab49" "Label5" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab51 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text 1 
    vTcl:DefineAlias "$site_3_0.lab51" "Label6" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab52 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text 2 
    vTcl:DefineAlias "$site_3_0.lab52" "Label10" vTcl:WidgetProc "MainGUI" 1
    ttk::separator $site_3_0.tSe53 \
        -orient vertical 
    vTcl:DefineAlias "$site_3_0.tSe53" "TSeparator1" vTcl:WidgetProc "MainGUI" 1
    ttk::separator $site_3_0.tSe54 \
        -orient vertical 
    vTcl:DefineAlias "$site_3_0.tSe54" "TSeparator2" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Training time:} 
    vTcl:DefineAlias "$site_3_0.lab43" "Label15" vTcl:WidgetProc "MainGUI" 1
    checkbutton $site_3_0.che44 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command OnChkStopTraining -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -justify left -text {Stop after} \
        -variable chVar_stop_tr 
    vTcl:DefineAlias "$site_3_0.che44" "chbtn_StopTraining" vTcl:WidgetProc "MainGUI" 1
    ttk::separator $site_3_0.tSe45 \
        -orient vertical 
    vTcl:DefineAlias "$site_3_0.tSe45" "TSeparator4" vTcl:WidgetProc "MainGUI" 1
    ttk::separator $site_3_0.tSe47 \
        -orient vertical 
    vTcl:DefineAlias "$site_3_0.tSe47" "TSeparator5" vTcl:WidgetProc "MainGUI" 1
    entry $site_3_0.ent48 \
        -background white -font TkFixedFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -justify center -selectbackground {#c4c4c4} \
        -selectforeground black -textvariable txtTrainingStop 
    vTcl:DefineAlias "$site_3_0.ent48" "txtTrainingStop" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab53 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font self.myFont_small -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {format- 00:00:00} 
    vTcl:DefineAlias "$site_3_0.lab53" "Label17" vTcl:WidgetProc "MainGUI" 1
    place $site_3_0.but39 \
        -in $site_3_0 -x 560 -y 10 -width 80 -relwidth 0 -height 50 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab46 \
        -in $site_3_0 -x 280 -y 10 -width 85 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.rad48 \
        -in $site_3_0 -x 330 -y 30 -anchor nw -bordermode ignore 
    place $site_3_0.rad49 \
        -in $site_3_0 -x 330 -y 50 -anchor nw -bordermode ignore 
    place $site_3_0.lab50 \
        -in $site_3_0 -x 220 -y 10 -width 57 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.but38 \
        -in $site_3_0 -x 560 -y 70 -width 80 -relwidth 0 -height 50 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex45 \
        -in $site_3_0 -x 230 -y 30 -width 60 -relwidth 0 -height 32 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex46 \
        -in $site_3_0 -x 290 -y 30 -width 42 -relwidth 0 -height 32 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex42 \
        -in $site_3_0 -x 230 -y 70 -width 60 -relwidth 0 -height 32 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex43 \
        -in $site_3_0 -x 290 -y 70 -width 42 -relwidth 0 -height 32 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.rad44 \
        -in $site_3_0 -x 330 -y 70 -anchor nw -bordermode ignore 
    place $site_3_0.rad45 \
        -in $site_3_0 -x 330 -y 90 -anchor nw -bordermode ignore 
    place $site_3_0.rad40 \
        -in $site_3_0 -x 10 -y 10 -anchor nw -bordermode ignore 
    place $site_3_0.rad43 \
        -in $site_3_0 -x 10 -y 30 -anchor nw -bordermode ignore 
    place $site_3_0.but44 \
        -in $site_3_0 -x 10 -y 60 -width 93 -relwidth 0 -height 62 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.rad38 \
        -in $site_3_0 -x 120 -y 60 -width 80 -relwidth 0 -height 22 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.rad39 \
        -in $site_3_0 -x 120 -y 40 -width 70 -height 22 -anchor nw \
        -bordermode ignore 
    place $site_3_0.lab49 \
        -in $site_3_0 -x 120 -y 10 -anchor nw -bordermode ignore 
    place $site_3_0.lab51 \
        -in $site_3_0 -x 210 -y 30 -width 19 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.lab52 \
        -in $site_3_0 -x 210 -y 70 -width 19 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.tSe53 \
        -in $site_3_0 -x 110 -y 10 -width 2 -relwidth 0 -height 100 \
        -anchor nw -bordermode inside 
    place $site_3_0.tSe54 \
        -in $site_3_0 -x 210 -y 10 -height 100 -anchor nw -bordermode inside 
    place $site_3_0.lab43 \
        -in $site_3_0 -x 430 -y 10 -anchor nw -bordermode ignore 
    place $site_3_0.che44 \
        -in $site_3_0 -x 430 -y 30 -anchor nw -bordermode ignore 
    place $site_3_0.tSe45 \
        -in $site_3_0 -x 420 -y 10 -height 100 -anchor nw -bordermode inside 
    place $site_3_0.tSe47 \
        -in $site_3_0 -x 550 -y 10 -height 100 -anchor nw -bordermode inside 
    place $site_3_0.ent48 \
        -in $site_3_0 -x 430 -y 82 -width 112 -relwidth 0 -height 27 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab53 \
        -in $site_3_0 -x 426 -y 60 -width 118 -height 24 -anchor nw \
        -bordermode ignore 
    button $top.but41 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onExit -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Exit 
    vTcl:DefineAlias "$top.but41" "btnExit" vTcl:WidgetProc "MainGUI" 1
    set site_3_0 $top.m43
    menu $site_3_0 \
        -activebackground {#d8d8d8} -activeforeground {#000000} \
        -background {#d9d9d9} -font TkMenuFont -foreground {#000000} \
        -tearoff 0 
    frame $top.fra52 \
        -borderwidth 2 -relief groove -background {#d9d9d9} \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 864 
    vTcl:DefineAlias "$top.fra52" "frmStat" vTcl:WidgetProc "MainGUI" 1
    set site_3_0 $top.fra52
    label $site_3_0.lab54 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Fish statistics} 
    vTcl:DefineAlias "$site_3_0.lab54" "Label3" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but55 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onStatClear -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Clear 
    vTcl:DefineAlias "$site_3_0.but55" "btnStatClear" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but56 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command OnRefresh -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Refresh 
    vTcl:DefineAlias "$site_3_0.but56" "btnDB_refresh" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab76 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Main folder:} 
    vTcl:DefineAlias "$site_3_0.lab76" "Label9" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab39 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Days back} 
    vTcl:DefineAlias "$site_3_0.lab39" "Label11" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex40 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 66 -wrap word 
    .top37.fra52.tex40 configure -font "TkTextFont"
    .top37.fra52.tex40 insert end text
    vTcl:DefineAlias "$site_3_0.tex40" "txtStatDaysBack" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex46 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 632 -wrap word 
    .top37.fra52.tex46 configure -font "TkTextFont"
    .top37.fra52.tex46 insert end text
    vTcl:DefineAlias "$site_3_0.tex46" "txtMainFolder" vTcl:WidgetProc "MainGUI" 1
    frame $site_3_0.fra44 \
        -borderwidth 2 -relief groove -background {#d9d9d9} -height 175 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 615 
    vTcl:DefineAlias "$site_3_0.fra44" "Frame1" vTcl:WidgetProc "MainGUI" 1
    set site_4_0 $site_3_0.fra44
    ttk::style configure Treeview.Heading -background #d9d9d9
    ttk::style configure Treeview.Heading -font "TkDefaultFont"
    vTcl::widgets::ttk::scrolledtreeview::CreateCmd $site_4_0.scr53 \
        -background {#d9d9d9} -height 15 -highlightbackground {#d9d9d9} \
        -highlightcolor black -width 30 
    vTcl:DefineAlias "$site_4_0.scr53" "DB" vTcl:WidgetProc "MainGUI" 1
        .top37.fra52.fra44.scr53.01 configure -columns {Col1}
        .top37.fra52.fra44.scr53.01 heading #0 -text {Tree}
        .top37.fra52.fra44.scr53.01 heading #0 -anchor center
        .top37.fra52.fra44.scr53.01 column #0 -width 293
        .top37.fra52.fra44.scr53.01 column #0 -minwidth 20
        .top37.fra52.fra44.scr53.01 column #0 -stretch 1
        .top37.fra52.fra44.scr53.01 column #0 -anchor w
        .top37.fra52.fra44.scr53.01 heading Col1 -text {Col1}
        .top37.fra52.fra44.scr53.01 heading Col1 -anchor center
        .top37.fra52.fra44.scr53.01 column Col1 -width 293
        .top37.fra52.fra44.scr53.01 column Col1 -minwidth 20
        .top37.fra52.fra44.scr53.01 column Col1 -stretch 1
        .top37.fra52.fra44.scr53.01 column Col1 -anchor w
    place $site_4_0.scr53 \
        -in $site_4_0 -x 10 -y 10 -width 600 -relwidth 0 -height 153 \
        -relheight 0 -anchor nw -bordermode ignore 
    label $site_3_0.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Log folder} 
    vTcl:DefineAlias "$site_3_0.lab43" "Label13" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab44 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Database file} 
    vTcl:DefineAlias "$site_3_0.lab44" "Label16" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex47 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -width 218 -wrap word 
    .top37.fra52.tex47 configure -font "TkTextFont"
    .top37.fra52.tex47 insert end text
    vTcl:DefineAlias "$site_3_0.tex47" "txtLogFolder" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex48 \
        -background white -font TkTextFont -foreground black \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -width 218 -wrap word 
    .top37.fra52.tex48 configure -font "TkTextFont"
    .top37.fra52.tex48 insert end text
    vTcl:DefineAlias "$site_3_0.tex48" "txtDBfile" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab55 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text Filter 
    vTcl:DefineAlias "$site_3_0.lab55" "Label12" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but57 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onOpenFolder -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -relief raised -text Open 
    vTcl:DefineAlias "$site_3_0.but57" "btnOpenLogFolder" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but58 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onShowDBFile -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -relief raised -text Show 
    vTcl:DefineAlias "$site_3_0.but58" "btnShowDBfile" vTcl:WidgetProc "MainGUI" 1
    ttk::separator $site_3_0.tSe43 \
        -orient vertical 
    vTcl:DefineAlias "$site_3_0.tSe43" "TSeparator3" vTcl:WidgetProc "MainGUI" 1
    place $site_3_0.lab54 \
        -in $site_3_0 -x 8 -y 8 -anchor nw -bordermode ignore 
    place $site_3_0.but55 \
        -in $site_3_0 -x 8 -y 229 -width 62 -relwidth 0 -height 30 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but56 \
        -in $site_3_0 -x 470 -y 220 -width 141 -relwidth 0 -height 38 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab76 \
        -in $site_3_0 -x 130 -y 10 -width 89 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab39 \
        -in $site_3_0 -x 100 -y 240 -width 77 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.tex40 \
        -in $site_3_0 -x 180 -y 240 -width 66 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex46 \
        -in $site_3_0 -x 220 -y 10 -width 632 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.fra44 \
        -in $site_3_0 -x 10 -y 40 -width 615 -relwidth 0 -height 175 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab43 \
        -in $site_3_0 -x 640 -y 48 -width 76 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.lab44 \
        -in $site_3_0 -x 640 -y 138 -width 95 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.tex47 \
        -in $site_3_0 -x 640 -y 70 -width 218 -relwidth 0 -height 26 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex48 \
        -in $site_3_0 -x 640 -y 160 -width 218 -relwidth 0 -height 26 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab55 \
        -in $site_3_0 -x 90 -y 220 -anchor nw -bordermode ignore 
    place $site_3_0.but57 \
        -in $site_3_0 -x 790 -y 100 -width 53 -relwidth 0 -height 32 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but58 \
        -in $site_3_0 -x 790 -y 190 -width 53 -relwidth 0 -height 32 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tSe43 \
        -in $site_3_0 -x 630 -y 40 -width 4 -relwidth 0 -height 210 \
        -anchor nw -bordermode ignore 
    frame $top.fra57 \
        -borderwidth 2 -relief groove -background {#d9d9d9} -height 131 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 204 
    vTcl:DefineAlias "$top.fra57" "frmCom" vTcl:WidgetProc "MainGUI" 1
    set site_3_0 $top.fra57
    label $site_3_0.lab58 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Motor test} 
    vTcl:DefineAlias "$site_3_0.lab58" "Label4" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but65 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command on1L -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text (1)L 
    vTcl:DefineAlias "$site_3_0.but65" "btnMotor1L" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but66 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command on1R -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text (1)R 
    vTcl:DefineAlias "$site_3_0.but66" "btnMotor1R" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but67 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command on2R -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text (2)R 
    vTcl:DefineAlias "$site_3_0.but67" "btnMotor2R" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but68 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command on2L -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text (2)L 
    vTcl:DefineAlias "$site_3_0.but68" "btnMotor2L" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab69 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Steps number} 
    vTcl:DefineAlias "$site_3_0.lab69" "Label7" vTcl:WidgetProc "MainGUI" 1
    entry $site_3_0.ent70 \
        -background white -font TkFixedFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black 
    vTcl:DefineAlias "$site_3_0.ent70" "txtStepNum" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but41 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onSetZero -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text {Set ZERO pos.} 
    vTcl:DefineAlias "$site_3_0.but41" "btnSetZero" vTcl:WidgetProc "MainGUI" 1
    place $site_3_0.lab58 \
        -in $site_3_0 -x 8 -y 8 -anchor nw -bordermode ignore 
    place $site_3_0.but65 \
        -in $site_3_0 -x 120 -y 20 -width 37 -relwidth 0 -height 48 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but66 \
        -in $site_3_0 -x 120 -y 70 -width 37 -relwidth 0 -height 48 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but67 \
        -in $site_3_0 -x 160 -y 70 -width 37 -relwidth 0 -height 48 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but68 \
        -in $site_3_0 -x 160 -y 20 -width 37 -relwidth 0 -height 48 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab69 \
        -in $site_3_0 -x 10 -y 30 -width 99 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.ent70 \
        -in $site_3_0 -x 10 -y 50 -width 80 -relwidth 0 -height 27 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but41 \
        -in $site_3_0 -x 10 -y 80 -width 107 -relwidth 0 -height 38 \
        -relheight 0 -anchor nw -bordermode ignore 
    frame $top.fra71 \
        -borderwidth 2 -relief groove -background {#d9d9d9} -height 265 \
        -highlightbackground {#d9d9d9} -highlightcolor black -width 865 
    vTcl:DefineAlias "$top.fra71" "frmLog" vTcl:WidgetProc "MainGUI" 1
    set site_3_0 $top.fra71
    label $site_3_0.lab73 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text Log 
    vTcl:DefineAlias "$site_3_0.lab73" "Label8" vTcl:WidgetProc "MainGUI" 1
    text $site_3_0.tex78 \
        -background white -font TkTextFont -foreground black -height 206 \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -insertbackground black -selectbackground {#c4c4c4} \
        -selectforeground black -undo 1 -width 852 -wrap word 
    .top37.fra71.tex78 configure -font "TkTextFont"
    .top37.fra71.tex78 insert end text
    vTcl:DefineAlias "$site_3_0.tex78" "txtMainLog" vTcl:WidgetProc "MainGUI" 1
    button $site_3_0.but38 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command onLogClear -font TkDefaultFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -pady 0 -text Clear 
    vTcl:DefineAlias "$site_3_0.but38" "frmLogClear" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab38 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Time runing:} 
    vTcl:DefineAlias "$site_3_0.lab38" "Label14" vTcl:WidgetProc "MainGUI" 1
    label $site_3_0.lab39 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkTextFont -foreground {#0000fe} \
        -highlightbackground {#d9d9d9} -highlightcolor black -justify left \
        -text 00:00 
    vTcl:DefineAlias "$site_3_0.lab39" "lblTimeCount" vTcl:WidgetProc "MainGUI" 1
    place $site_3_0.lab73 \
        -in $site_3_0 -x 8 -y 8 -anchor nw -bordermode ignore 
    place $site_3_0.tex78 \
        -in $site_3_0 -x 8 -y 32 -width 852 -relwidth 0 -height 206 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but38 \
        -in $site_3_0 -x 10 -y 240 -width 70 -relwidth 0 -height 22 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab38 \
        -in $site_3_0 -x 460 -y 8 -width 91 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.lab39 \
        -in $site_3_0 -x 560 -y 8 -width 211 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    set site_3_0 $top.m45
    menu $site_3_0 \
        -activebackground {#d8d8d8} -activeforeground {#000000} \
        -background {#d9d9d9} -font TkMenuFont -foreground {#000000} \
        -tearoff 0 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.fra38 \
        -in $top -x 220 -y 290 -width 654 -relwidth 0 -height 131 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $top.but41 \
        -in $top -x 690 -y 700 -width 177 -relwidth 0 -height 40 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.fra52 \
        -in $top -x 10 -y 10 -width 865 -relwidth 0 -height 270 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.fra57 \
        -in $top -x 10 -y 290 -width 204 -relwidth 0 -height 131 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.fra71 \
        -in $top -x 10 -y 430 -width 865 -relwidth 0 -height 265 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top37 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

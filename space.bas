Rem working keypressed
Global oKeyHandler As Object
Sub MainKeyHandler
    oController = ThisComponent.getCurrentController()
Rem only if not yet running
    if isNull(oKeyHandler) then
        oKeyHandler = CreateUnoListener("KeyHandler_", "com.sun.star.awt.XKeyHandler")
        oController.addKeyHandler(oKeyHandler)
        msgbox "Handler Started"
    endif
Rem    oPresentation = ThisComponent.Presentation
Rem    oPresentation.start()
End Sub

Sub StopKeyHandler
    oController = ThisComponent.getCurrentController()
    If not IsNull(oKeyHandler) then 'only if still running
        oController.removeKeyHandler(oKeyHandler)
        oKeyHandler = Nothing 'To know later this handler has stopped.
        msgbox "Handler Stopped"
    End If
End Sub

Function KeyHandler_keyPressed( oEvent ) as Boolean
Rem Wait 200
  If oEvent.keyCode = com.sun.star.awt.Key.SPACE Then
     msgbox "Space was pressed"
     KeyHandler_keyPressed = false
  ElseIf oEvent.keyCode <> com.sun.star.awt.Key.SPACE Then
'     msgbox "Not Space was pressed"
     KeyHandler_keyPressed = false
  End If
End Function

Function KeyHandler_keyReleased( oEvent ) as Boolean
KeyHandler_keyReleased = true
End Function

sub KeyHandler_disposing(oEvent)
end sub
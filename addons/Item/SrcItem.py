main = """package <package>;

<imports>

public class <classname> extends Item{

private final String name = "<unlocalizedName>";

    public <classname>() {
        GameRegistry.registerItem(this, name);
        this.setUnlocalizedName(name);
        this.setCreativeTab(<creativeTab>);
    }
	
	public String getName() {
		return name;
	}

}"""

imports = """import net.minecraft.item.Item;
import net.minecraftforge.fml.common.registry.GameRegistry;"""

commonInit = """<instancename> = new <classname>();"""
    
clientInit = """			Minecraft.getMinecraft().getRenderItem().getItemModelMesher().register(<instancename>, 0, new ModelResourceLocation("<modid>:<unlocalizedName>", "inventory"));"""

json = """{
    "parent": "builtin/generated",
    "textures": {
        "layer0": "<modid>:items/<unlocalizedName>"
    },
    "display": {
        "thirdperson": {
            "rotation": [ -90, 0, 0 ],
            "translation": [ 0, 1, -3 ],
            "scale": [ 0.55, 0.55, 0.55 ]
        },
        "firstperson": {
            "rotation": [ 0, -135, 25 ],
            "translation": [ 0, 4, 2 ],
            "scale": [ 1.7, 1.7, 1.7 ]
        }
    }
}"""
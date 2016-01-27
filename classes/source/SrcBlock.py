main = """package <package>;

<imports>

public class <classname> extends Block {
	
	private final String name = "<unlocalizedName>";

	public <classname>() {
		super(<material>);
		GameRegistry.registerBlock(this, name);
		this.setUnlocalizedName(name);
		this.setCreativeTab(<creativeTab>);
		this.setHardness(<hardness>F);
		this.setResistance(<resistance>F);
		this.setHarvestLevel("<tool>", <harvestLevel>);
	}
	
<additionalAttributes>

}
"""

imports = """import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraftforge.fml.common.registry.GameRegistry;"""

commonInit = """<instancename> = new <classname>();"""

clientInit = """			Minecraft.getMinecraft().getRenderItem().getItemModelMesher().register(Item.getItemFromBlock(<instancename>), 0, new ModelResourceLocation("<modid>:<unlocalizedName>", "inventory"));"""

blockstatesJson = """{
    "variants": {
        "normal": { "model": "<modid>:<unlocalizedName>" }
    }
}"""

blockmodelJson = """{
    "parent": "block/cube_all",
    "textures": {
        "all": "<modid>:blocks/<unlocalizedName>"
    }
}"""

itemmodelJson = """{
    "parent":"<modid>:block/<unlocalizedName>",
    "display": {
        "thirdperson": {
            "rotation": [ 10, -45, 170 ],
            "translation": [ 0, 1.5, -2.75 ],
            "scale": [ 0.375, 0.375, 0.375 ]
        }
    }
}"""

renderLayerTransparent = """@SideOnly(Side.CLIENT)
    public EnumWorldBlockLayer getBlockLayer()
    {
        return EnumWorldBlockLayer.<layer>;
    }
    
    @Override
    public boolean isOpaqueCube() {
        return false;
    }"""